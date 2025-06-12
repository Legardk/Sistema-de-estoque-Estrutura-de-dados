# Importa json para salvar e carregar a fila de/para arquivos.
# Importa deque (Double-Ended Queue) da biblioteca collections, que é uma estrutura de dados
# otimizada para adicionar e remover elementos de suas extremidades (ideal para filas e pilhas).
# Importa a classe Pedido.
import json
from collections import deque
from Pedido import Pedido

# A classe FilaPedidos gerencia os pedidos que aguardam processamento.
# Utiliza a estrutura de dados "Fila" (Queue), que segue a lógica FIFO (First-In, First-Out).
# O primeiro pedido que chega é o primeiro a ser processado.
class FilaPedidos:
    """
    Gerencia uma fila de pedidos pendentes e um histórico de pedidos atendidos.
    """
    def __init__(self):
        """
        Inicializa a fila de pedidos e o histórico de atendidos usando 'deque'.
        """
        self.fila = deque()
        self.historico_atendidos = deque()
        
    def adicionar_pedido(self, pedido):
        """
        Adiciona um novo pedido ao final da fila.

        Args:
            pedido (Pedido): O objeto Pedido a ser adicionado.
        """
        self.fila.append(pedido)
        
    def processar_pedido(self, estoque):
        """
        Processa o primeiro pedido da fila.

        Verifica se há estoque suficiente. Se houver, remove os itens do estoque
        e move o pedido para o histórico. Se não, o pedido volta para o início da fila.

        Args:
            estoque (Estoque): O objeto de estoque para verificação e remoção de itens.

        Returns:
            bool: True se o pedido foi processado com sucesso, False caso contrário.
                  Retorna None se a fila estiver vazia.
        """
        # Verifica se há pedidos na fila.
        if self.fila:
            # Pega o primeiro pedido da fila (FIFO).
            pedido = self.fila.popleft()
            # Verifica a quantidade total do produto disponível no estoque.
            total_disponivel = estoque.contar_por_produto(pedido.codigo_produto)
            
            # Se a quantidade em estoque for suficiente...
            if total_disponivel >= pedido.quantidade:
                # Tenta remover a quantidade solicitada do estoque.
                remocao_sucesso = estoque.remover_engradado(pedido.codigo_produto, pedido.quantidade)
                if remocao_sucesso:
                    print(f"Pedido de {pedido.solicitante} atendido!")
                    # Adiciona o pedido ao histórico de pedidos atendidos.
                    self.historico_atendidos.append(pedido)
                    return True
                else:
                    # Se ocorrer um erro inesperado na remoção, devolve o pedido à fila.
                    print(f"Erro inesperado ao remover do estoque para o pedido de {pedido.solicitante}.")
                    self.fila.appendleft(pedido)
                    return False
            # Se não houver estoque suficiente...
            else:
                print(f"Estoque insuficiente para atender pedido de {pedido.solicitante} (faltam {pedido.quantidade - total_disponivel} unidades do produto {pedido.codigo_produto}).")
                # Devolve o pedido ao início da fila para ser tentado novamente mais tarde.
                self.fila.appendleft(pedido)
                return False
        return None

    def salvar_pedidos(self, nome_arquivo):
        """
        Salva a fila de pedidos pendentes e o histórico de atendidos em um arquivo JSON.

        Args:
            nome_arquivo (str): O caminho do arquivo para salvar os dados.
        """
        # Cria um dicionário contendo a fila e o histórico.
        dados_a_salvar = {
            'fila': [p.para_dicionario() for p in self.fila],
            'historico_atendidos': [p.para_dicionario() for p in self.historico_atendidos]
        }
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_a_salvar, f, ensure_ascii=False, indent=4)

    def carregar_pedidos(self, nome_arquivo):
        """
        Carrega a fila de pedidos e o histórico de um arquivo JSON.

        Args:
            nome_arquivo (str): O caminho do arquivo para carregar os dados.
        """
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                dados_carregados = json.load(f)
                
                # Para compatibilidade com versões antigas do arquivo JSON.
                if isinstance(dados_carregados, list):
                    # Formato antigo era apenas uma lista de pedidos.
                    fila_para_carregar = dados_carregados
                    historico_para_carregar = []
                else:
                    # Formato novo é um dicionário com 'fila' e 'historico_atendidos'.
                    fila_para_carregar = dados_carregados.get('fila', [])
                    historico_para_carregar = dados_carregados.get('historico_atendidos', [])
                
                # Carrega os pedidos pendentes.
                for d in fila_para_carregar:
                    self.adicionar_pedido(Pedido(d['codigo_produto'], d['quantidade'], d['data_solicitacao'], d['solicitante']))
                
                # Carrega o histórico de pedidos atendidos.
                for d in historico_para_carregar:
                    self.historico_atendidos.append(Pedido(d['codigo_produto'], d['quantidade'], d['data_solicitacao'], d['solicitante']))
                
        except FileNotFoundError:
            print(f"Arquivo de pedidos '{nome_arquivo}' não encontrado. Iniciando com fila e histórico vazios.")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Erro ao ler o arquivo de pedidos '{nome_arquivo}' ({e}). Iniciando com fila e histórico vazios.")

    def obter_historico_pedidos_atendidos(self):
        """
        Retorna uma lista com o histórico de todos os pedidos que já foram atendidos.

        Returns:
            list: Uma lista de objetos Pedido.
        """
        return list(self.historico_atendidos)