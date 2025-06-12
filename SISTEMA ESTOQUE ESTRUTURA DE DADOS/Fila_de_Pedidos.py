import json
from collections import deque
from Pedido import Pedido
from Pilha import Pilha # Embora não usado diretamente, é bom manter para consistência

class FilaPedidos:
    
    def __init__(self):
        self.fila = deque()
        
    def adicionar_pedido(self, pedido):
        self.fila.append(pedido)
        
    def processar_pedido(self, estoque):
        if self.fila:
            pedido = self.fila.popleft()
            retirados = estoque.remover_engradado(pedido.codigo_produto, pedido.quantidade)
            if retirados is not None:
                print(f"Pedido de {pedido.solicitante} atendido!")
                return True
            
            else:
                print(f"produto insuficiente para atender pedido de {pedido.solicitante}.")
                self.fila.appendleft(pedido) # Devolve o pedido para o início da fila
                return False
        return None

    def salvar_pedidos(self, nome_arquivo):
        """Salva a fila de pedidos atual em um arquivo JSON."""
        lista_pedidos = [p.para_dicionario() for p in self.fila]
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(lista_pedidos, f, ensure_ascii=False, indent=4)

    def carregar_pedidos(self, nome_arquivo):
        """Carrega os pedidos de um arquivo JSON para a fila."""
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                lista_dict = json.load(f)
                for d in lista_dict:
                    pedido = Pedido(
                        d['codigo_produto'],
                        d['quantidade'],
                        d['data_solicitacao'],
                        d['solicitante']
                    )
                    self.adicionar_pedido(pedido)
        except FileNotFoundError:
            print(f"Arquivo de pedidos '{nome_arquivo}' não encontrado. Iniciando com fila vazia.")
        except (json.JSONDecodeError, KeyError):
            print(f"Erro ao ler o arquivo de pedidos '{nome_arquivo}'. Verifique o formato. Iniciando com fila vazia.")