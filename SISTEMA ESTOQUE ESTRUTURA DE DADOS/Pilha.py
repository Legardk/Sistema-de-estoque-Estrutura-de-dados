# Importa a classe Engradado para que a Pilha possa armazenar objetos desse tipo.
from Engradado import Engradado

# A classe Pilha implementa a estrutura de dados "Pilha" (Stack).
# No nosso sistema, ela representa uma pilha física de engradados em uma prateleira do estoque.
# Segue a lógica LIFO (Last-In, First-Out), ou seja, o último engradado a entrar é o primeiro a sair.
class Pilha:
    """
    Implementa uma Pilha para armazenar engradados.
    A pilha tem uma capacidade máxima e só pode conter engradados do mesmo produto.
    """
    def __init__(self):
        """
        Inicializa uma nova Pilha vazia.
        'engradados' é uma lista que armazenará os objetos Engradado.
        """
        self.engradados = []

    def adicionar(self, engradado):
        """
        Adiciona um engradado ao topo da pilha.

        Regras:
        1. A pilha não pode ter mais de 5 engradados.
        2. Um engradado só pode ser adicionado se a pilha estiver vazia ou se o engradado
           do topo for do mesmo produto.

        Args:
            engradado (Engradado): O engradado a ser adicionado.

        Returns:
            bool: True se o engradado foi adicionado com sucesso, False caso contrário.
        """
        # Verifica se a capacidade máxima da pilha (5 engradados) foi atingida.
        if len(self.engradados) < 5:
            # Se a pilha está vazia ou o produto do engradado é o mesmo do topo da pilha,
            # o novo engradado é adicionado.
            if not self.engradados or self.engradados[-1].produto_codigo == engradado.produto_codigo:
                self.engradados.append(engradado)
                return True
        # Retorna False se a capacidade foi excedida ou se o produto é diferente.
        return False
    
    def remover(self):
        """
        Remove e retorna o engradado do topo da pilha (LIFO).

        Returns:
            Engradado: O engradado removido, ou None se a pilha estiver vazia.
        """
        if self.engradados:
            return self.engradados.pop()
        return None

    def topo(self):
        """
        Retorna o engradado do topo da pilha sem removê-lo.

        Returns:
            Engradado: O engradado do topo, ou None se a pilha estiver vazia.
        """
        if self.engradados:
            return self.engradados[-1]
        
    def esta_vazia(self):
        """
        Verifica se a pilha não contém engradados.

        Returns:
            bool: True se a pilha estiver vazia, False caso contrário.
        """
        return len(self.engradados) == 0