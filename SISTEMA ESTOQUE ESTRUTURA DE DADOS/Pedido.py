# Importa datetime para trabalhar com a data da solicitação do pedido.
from datetime import datetime

# A classe Pedido representa uma solicitação de um cliente.
# Contém as informações de qual produto foi solicitado, a quantidade e por quem.
class Pedido:
    """
    Representa um pedido de um cliente.
    """
    def __init__(self , codigo_produto , quantidade , data_solicitacao , solicitante ):
        """
        Inicializa um novo objeto Pedido.

        Args:
            codigo_produto (str): Código do produto solicitado.
            quantidade (int): Quantidade do produto solicitado.
            data_solicitacao (str): Data em que o pedido foi feito (formato "YYYY-MM-DD").
            solicitante (str): Nome de quem fez o pedido.
        """
        self.codigo_produto = codigo_produto
        self.quantidade = quantidade
        # Converte a string da data para um objeto datetime.
        self.data_solicitacao = datetime.strptime(data_solicitacao , "%Y-%m-%d")
        self.solicitante = solicitante
    
    def para_dicionario(self):
        """
        Converte o objeto Pedido para um dicionário, facilitando a gravação em JSON.

        Returns:
            dict: Um dicionário representando o pedido.
        """
        return {
            'codigo_produto': self.codigo_produto,
            'quantidade': self.quantidade,
            # Converte o objeto datetime de volta para uma string para salvar no JSON.
            'data_solicitacao': self.data_solicitacao.strftime("%Y-%m-%d"),
            'solicitante': self.solicitante
        }