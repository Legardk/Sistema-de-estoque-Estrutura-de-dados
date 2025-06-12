# A classe Engradado representa uma unidade de armazenamento físico no estoque.
# Cada engradado contém uma certa quantidade de um único tipo de produto.
class Engradado:
    """
    Representa um engradado contendo uma quantidade específica de um produto.
    """
    def __init__(self, produto_codigo, quantidade):
        """
        Inicializa um novo Engradado.

        Args:
            produto_codigo (str): O código do produto contido no engradado.
            quantidade (int): O número de unidades do produto no engradado.
        """
        self.produto_codigo = produto_codigo
        self.quantidade = quantidade