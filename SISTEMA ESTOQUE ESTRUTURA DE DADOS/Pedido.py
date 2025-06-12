from datetime import datetime

class Pedido:
    def __init__(self , codigo_produto , quantidade , data_solicitacao , solicitante ):
        self.codigo_produto = codigo_produto
        self.quantidade = quantidade
        self.data_solicitacao = datetime.strptime(data_solicitacao , "%Y-%m-%d")
        self.solicitante = solicitante
    
    def para_dicionario(self):
        """Converte o objeto Pedido para um dicionário para salvar em JSON."""
        return {
            'codigo_produto': self.codigo_produto,
            'quantidade': self.quantidade,
            'data_solicitacao': self.data_solicitacao.strftime("%Y-%m-%d"),
            'solicitante': self.solicitante
        }