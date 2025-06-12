import json
from Pilha import Pilha # O estoque é composto por Pilhas de engradados.
from Pedido import Pedido
from Engradado import Engradado
from datetime import datetime, timedelta # Para o relatório de validade.

# A classe Estoque é o coração do sistema. Ela gerencia a estrutura de armazenamento.
# A estrutura escolhida foi uma Matriz (lista de listas) 8x5, simulando um armazém com
# 8 corredores e 5 prateleiras (ou posições) em cada um.
# Cada posição da matriz contém uma Pilha de engradados.
class Estoque:
    """
    Gerencia o estoque físico, representado por uma matriz de pilhas de engradados.
    """
    def __init__(self):
        """
        Inicializa o estoque como uma matriz 8x5. Cada célula da matriz contém uma Pilha.
        """
        # Cria uma matriz 8x5 onde cada elemento é uma nova instância da classe Pilha.
        self.matriz = [[Pilha() for _ in range(5)] for _ in range(8)]
        
    def adicionar_engradado(self, engradado):
        """
        Adiciona um engradado ao estoque.

        Percorre a matriz procurando uma pilha que possa aceitar o engradado
        (de acordo com as regras da classe Pilha).

        Args:
            engradado (Engradado): O engradado a ser adicionado.

        Returns:
            bool: True se adicionado com sucesso, False se o estoque estiver cheio.
        """
        # Itera pelas linhas (i) e colunas (j) da matriz.
        for i, linha in enumerate(self.matriz):
            for j, pilha in enumerate(linha):
                # Tenta adicionar o engradado na pilha atual.
                # O método pilha.adicionar() já contém a lógica de validação.
                if pilha.adicionar(engradado):
                    print(f"Engradado adicionado na posição [{i}][{j}]")
                    return True
        # Se percorreu toda a matriz e não conseguiu adicionar, o estoque está cheio.
        return False
        
    def remover_engradado(self, produto_codigo, quantidade):
        """
        Remove uma quantidade específica de um produto do estoque.

        Percorre toda a matriz procurando pelo produto. Como os engradados estão
        em pilhas, a remoção segue a regra LIFO (começa pelo topo).

        Args:
            produto_codigo (str): O código do produto a ser removido.
            quantidade (int): A quantidade de unidades a ser removida.

        Returns:
            bool: True se a remoção foi bem-sucedida, False caso contrário.
        """
        quantidade_a_remover = quantidade
        
        # Percorre a matriz para encontrar os engradados do produto.
        for linha_idx, linha in enumerate(self.matriz):
            for pilha_idx, pilha in enumerate(linha):
                # Enquanto a pilha tiver engradados do produto desejado e ainda faltar remover itens...
                while pilha.topo() and pilha.topo().produto_codigo == produto_codigo and quantidade_a_remover > 0:
                    engradado_topo = pilha.topo()
                    
                    # Se a quantidade no engradado do topo for menor ou igual à que precisamos...
                    if engradado_topo.quantidade <= quantidade_a_remover:
                        # Remove o engradado inteiro.
                        removido = pilha.remover()
                        quantidade_a_remover -= removido.quantidade
                        print(f"  Removido engradado completo de {removido.quantidade} unidades do produto {produto_codigo} da posição [{linha_idx}][{pilha_idx}].")
                    else:
                        # Se o engradado do topo tem mais itens do que precisamos...
                        # Remove apenas a quantidade necessária do engradado.
                        engradado_topo.quantidade -= quantidade_a_remover
                        print(f"  Removidas {quantidade_a_remover} unidades do produto {produto_codigo} do engradado na posição [{linha_idx}][{pilha_idx}].")
                        quantidade_a_remover = 0 # Zera a quantidade, pois já removemos tudo.
                        
                    # Se já removemos a quantidade total, podemos sair da função.
                    if quantidade_a_remover == 0:
                        return True
        
        # Se o loop terminar e ainda faltar remover itens, o estoque era insuficiente.
        if quantidade_a_remover > 0:
            print(f"Estoque insuficiente. Não foi possível remover a quantidade total solicitada.")
            # Este retorno é um fallback, a verificação prévia no menu deve evitar isso.
            return False
        
        return True

    def visualizar(self):
        """
        Imprime uma representação textual do estado atual do estoque.
        Mostra o que há no topo de cada pilha.
        """
        for i, linha in enumerate(self.matriz):
            print(f"Linha {i}:")
            for j, pilha in enumerate(linha):
                topo = pilha.topo()
                if topo:
                    # Mostra o código do produto, quantos engradados há na pilha, e a quantidade no engradado do topo.
                    print(f"  Coluna {j}: {topo.produto_codigo} x {len(pilha.engradados)} engradados (Topo: {topo.quantidade} unidades)")
                else:
                    print(f"  Coluna {j}: Vazia")
                    
    def contar_por_produto(self, produto_codigo):
        """
        Conta a quantidade total de unidades de um produto específico em todo o estoque.

        Args:
            produto_codigo (str): O código do produto a ser contado.

        Returns:
            int: O total de unidades do produto em estoque.
        """
        total = 0
        # Percorre cada pilha e cada engradado, somando as quantidades.
        for linha in self.matriz:
            for pilha in linha:
                for eng in pilha.engradados:
                    if eng.produto_codigo == produto_codigo:
                        total += eng.quantidade
        return total
    
    def salvar_estoque(self, nome_arquivo):
        """
        Salva o estado atual do estoque em um arquivo JSON.
        """
        matriz_serializavel = []
        for linha in self.matriz:
            linha_serializavel = []
            for pilha in linha:
                # Converte cada engradado em um dicionário.
                pilha_serializavel = [
                    {'produto_codigo': eng.produto_codigo, 'quantidade': eng.quantidade} 
                    for eng in pilha.engradados
                ]
                linha_serializavel.append(pilha_serializavel)
            matriz_serializavel.append(linha_serializavel)
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(matriz_serializavel, f, ensure_ascii=False, indent=4)

    def carregar_estoque(self, nome_arquivo):
        """
        Carrega o estado do estoque de um arquivo JSON.
        """
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                matriz_serializavel = json.load(f)
                if not matriz_serializavel: return

                # Recria a estrutura da matriz e das pilhas.
                self.matriz = [[Pilha() for _ in range(5)] for _ in range(8)]
                for i, linha_serializavel in enumerate(matriz_serializavel):
                    for j, pilha_serializavel in enumerate(linha_serializavel):
                        for dados_engradado in pilha_serializavel:
                            # Recria cada objeto Engradado e o adiciona à pilha correta.
                            engradado = Engradado(dados_engradado['produto_codigo'], dados_engradado['quantidade'])
                            self.matriz[i][j].adicionar(engradado)
        except FileNotFoundError:
            pass # Se o arquivo não existe, simplesmente começa com o estoque vazio.
        except (json.JSONDecodeError, KeyError):
            print(f"Erro ao ler o arquivo de estoque '{nome_arquivo}'. Iniciando com estoque vazio.")

    # --- Métodos para Relatórios ---

    def _obter_engradados_recursivo(self, i, j, engradados_encontrados):
        """
        Função auxiliar RECURSIVA para percorrer a matriz e coletar todos os engradados.

        Args:
            i (int): Índice da linha atual.
            j (int): Índice da coluna atual.
            engradados_encontrados (list): Lista para acumular os engradados.
        """
        # Caso base da recursão: quando o índice 'i' ultrapassa o número de linhas.
        if i >= len(self.matriz):
            return

        # Se o índice 'j' ultrapassa o número de colunas, passa para a próxima linha.
        if j >= len(self.matriz[i]):
            self._obter_engradados_recursivo(i + 1, 0, engradados_encontrados)
            return

        # Adiciona os engradados da pilha atual à lista.
        engradados_encontrados.extend(self.matriz[i][j].engradados)
        
        # Chamada recursiva para a próxima coluna na mesma linha.
        self._obter_engradados_recursivo(i, j + 1, engradados_encontrados)

    def obter_todos_engradados(self):
        """
        Retorna uma lista plana com todos os engradados no estoque, usando recursividade.

        Returns:
            list: Uma lista de todos os objetos Engradado no estoque.
        """
        todos_engradados = []
        # Inicia o processo recursivo a partir da posição [0][0].
        self._obter_engradados_recursivo(0, 0, todos_engradados)
        return todos_engradados

    def obter_produtos_proximos_vencimento(self, produtos_cadastrados, dias=30):
        """
        Identifica produtos no estoque que estão próximos da data de vencimento.

        Args:
            produtos_cadastrados (list): A lista de todos os produtos cadastrados.
            dias (int): O número de dias para considerar como "próximo ao vencimento".

        Returns:
            list: Uma lista de dicionários, cada um representando um item próximo a vencer.
        """
        produtos_vencendo = []
        data_limite = datetime.now() + timedelta(days=dias)
        
        # Usa a função recursiva para obter todos os engradados de uma só vez.
        engradados_no_estoque = self.obter_todos_engradados()

        # Compara a data de validade de cada produto no estoque com a data limite.
        for engradado in engradados_no_estoque:
            for produto_info in produtos_cadastrados:
                if produto_info.codigo == engradado.produto_codigo:
                    if produto_info.data_validade <= data_limite:
                        produtos_vencendo.append({
                            'codigo': produto_info.codigo, 'nome': produto_info.nome,
                            'lote': produto_info.lote, 'quantidade_engradado': engradado.quantidade,
                            'data_validade': produto_info.data_validade.strftime("%Y-%m-%d")
                        })
                    break 
        return produtos_vencendo

    def obter_itens_em_falta(self, produtos_cadastrados, limite_baixo=10):
        """
        Identifica produtos cujo nível de estoque está abaixo de um limite mínimo.

        Args:
            produtos_cadastrados (list): A lista de todos os produtos cadastrados.
            limite_baixo (int): O nível de estoque considerado crítico.

        Returns:
            list: Uma lista de dicionários, cada um representando um item com estoque baixo.
        """
        itens_em_falta = []
        for produto in produtos_cadastrados:
            # Conta o total em estoque para cada produto cadastrado.
            total_em_estoque = self.contar_por_produto(produto.codigo)
            if total_em_estoque < limite_baixo:
                itens_em_falta.append({
                    'codigo': produto.codigo, 'nome': produto.nome,
                    'total_em_estoque': total_em_estoque, 'limite_baixo': limite_baixo,
                    'faltando': limite_baixo - total_em_estoque
                })
        return itens_em_falta