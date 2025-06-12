import json
from collections import deque
from Pedido import Pedido

class FilaPedidos:
    
    def __init__(self):
        self.fila = deque()
        self.historico_atendidos = deque()
        
    def adicionar_pedido(self, pedido):
        self.fila.append(pedido)
        
    def processar_pedido(self, estoque):
        if self.fila:
            pedido = self.fila.popleft()
            total_disponivel = estoque.contar_por_produto(pedido.codigo_produto)
            if total_disponivel >= pedido.quantidade:
                remocao_sucesso = estoque.remover_engradado(pedido.codigo_produto, pedido.quantidade)
                if remocao_sucesso:
                    print(f"Pedido de {pedido.solicitante} atendido!")
                    self.historico_atendidos.append(pedido)
                    return True
                else:
                    print(f"Erro inesperado ao remover do estoque para o pedido de {pedido.solicitante}.")
                    self.fila.appendleft(pedido)
                    return False
            else:
                print(f"Estoque insuficiente para atender pedido de {pedido.solicitante} (faltam {pedido.quantidade - total_disponivel} unidades do produto {pedido.codigo_produto}).")
                self.fila.appendleft(pedido)
                return False
        return None

    def salvar_pedidos(self, nome_arquivo):
        """Salva a fila de pedidos atual e o histórico em um arquivo JSON."""
        dados_a_salvar = {
            'fila': [p.para_dicionario() for p in self.fila],
            'historico_atendidos': [p.para_dicionario() for p in self.historico_atendidos]
        }
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_a_salvar, f, ensure_ascii=False, indent=4)

    def carregar_pedidos(self, nome_arquivo):
        """Carrega os pedidos e o histórico de um arquivo JSON para a fila."""
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                dados_carregados = json.load(f)
                
                # NOVO: Verifica se o JSON é uma lista (formato antigo) ou um dicionário (novo formato)
                if isinstance(dados_carregados, list):
                    # Se for uma lista (formato antigo), trata como a fila de pedidos
                    fila_para_carregar = dados_carregados
                    historico_para_carregar = [] # Historico estaria vazio no formato antigo
                else:
                    # Se for um dicionário (novo formato), obtém as chaves 'fila' e 'historico_atendidos'
                    fila_para_carregar = dados_carregados.get('fila', [])
                    historico_para_carregar = dados_carregados.get('historico_atendidos', [])
                
                for d in fila_para_carregar:
                    pedido = Pedido(
                        d['codigo_produto'],
                        d['quantidade'],
                        d['data_solicitacao'],
                        d['solicitante']
                    )
                    self.adicionar_pedido(pedido)
                
                for d in historico_para_carregar:
                    pedido = Pedido(
                        d['codigo_produto'],
                        d['quantidade'],
                        d['data_solicitacao'],
                        d['solicitante']
                    )
                    self.historico_atendidos.append(pedido)
                
        except FileNotFoundError:
            print(f"Arquivo de pedidos '{nome_arquivo}' não encontrado. Iniciando com fila e histórico vazios.")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Erro ao ler o arquivo de pedidos '{nome_arquivo}' ({e}). Verifique o formato. Iniciando com fila e histórico vazios.")

    def obter_historico_pedidos_atendidos(self):
        """Retorna o histórico de pedidos atendidos."""
        return list(self.historico_atendidos)