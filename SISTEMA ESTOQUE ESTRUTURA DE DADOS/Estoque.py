import json
from Pilha import Pilha
from Pedido import Pedido
from Engradado import Engradado
from datetime import datetime, timedelta # Importar timedelta

class Estoque:
    def __init__(self):
        self.matriz = [[Pilha() for _ in range(5)] for _ in range(8)]
        
    def adicionar_engradado(self, engradado):
        for i, linha in enumerate(self.matriz):
            for j, pilha in enumerate(linha):
                if pilha.adicionar(engradado):
                    print(f"Engradado adicionado na posição [{i}][{j}]")
                    return True
        return False
        
    def remover_engradado(self, produto_codigo, quantidade):
        quantidade_a_remover = quantidade
        
        for linha_idx, linha in enumerate(self.matriz):
            for pilha_idx, pilha in enumerate(linha):
                while pilha.topo() and pilha.topo().produto_codigo == produto_codigo and quantidade_a_remover > 0:
                    engradado_topo = pilha.topo()
                    
                    if engradado_topo.quantidade <= quantidade_a_remover:
                        removido = pilha.remover()
                        quantidade_a_remover -= removido.quantidade
                        print(f"  Removido engradado completo de {removido.quantidade} unidades do produto {produto_codigo} da posição [{linha_idx}][{pilha_idx}].")
                    else:
                        engradado_topo.quantidade -= quantidade_a_remover
                        print(f"  Removidas {quantidade_a_remover} unidades do produto {produto_codigo} do engradado na posição [{linha_idx}][{pilha_idx}].")
                        quantidade_a_remover = 0
                        
                    if quantidade_a_remover == 0:
                        return True
        
        if quantidade_a_remover > 0:
            print(f"Estoque insuficiente. Não foi possível remover {quantidade - quantidade_a_remover} unidades do produto {produto_codigo}.")
            return False
        
        return True

    def visualizar(self):
        for i, linha in enumerate(self.matriz):
            print(f"Linha {i}:")
            for j, pilha in enumerate(linha):
                topo = pilha.topo()
                if topo:
                    print(f"  Coluna {j}: {topo.produto_codigo} x {len(pilha.engradados)} engradados (Topo: {topo.quantidade} unidades)")
                else:
                    print(f"  Coluna {j}: Vazia")
                    
    def contar_por_produto(self, produto_codigo):
        total = 0
        for linha in self.matriz:
            for pilha in linha:
                for eng in pilha.engradados:
                    if eng.produto_codigo == produto_codigo:
                        total += eng.quantidade
        return total
    
    def salvar_estoque(self, nome_arquivo):
        """Salva o estado atual do estoque em um arquivo JSON."""
        matriz_serializavel = []
        for linha in self.matriz:
            linha_serializavel = []
            for pilha in linha:
                pilha_serializavel = [
                    {'produto_codigo': eng.produto_codigo, 'quantidade': eng.quantidade} 
                    for eng in pilha.engradados
                ]
                linha_serializavel.append(pilha_serializavel)
            matriz_serializavel.append(linha_serializavel)
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(matriz_serializavel, f, ensure_ascii=False, indent=4)

    def carregar_estoque(self, nome_arquivo):
        """Carrega o estado do estoque de um arquivo JSON."""
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                matriz_serializavel = json.load(f)
                if not matriz_serializavel: return

                self.matriz = [[Pilha() for _ in range(5)] for _ in range(8)]
                for i, linha_serializavel in enumerate(matriz_serializavel):
                    for j, pilha_serializavel in enumerate(linha_serializavel):
                        for dados_engradado in pilha_serializavel:
                            engradado = Engradado(
                                dados_engradado['produto_codigo'],
                                dados_engradado['quantidade']
                            )
                            self.matriz[i][j].adicionar(engradado)
        except FileNotFoundError:
            pass
        except (json.JSONDecodeError, KeyError):
            print(f"Erro ao ler o arquivo de estoque '{nome_arquivo}'. Verifique o formato. Iniciando com estoque vazio.")

    # --- Novos métodos para relatórios ---

    def _obter_engradados_recursivo(self, i, j, engradados_encontrados):
        """Função auxiliar recursiva para percorrer os engradados."""
        if i >= len(self.matriz):
            return # Base da recursão: todas as linhas foram percorridas

        if j >= len(self.matriz[i]):
            # Se todas as colunas da linha atual foram percorridas, vai para a próxima linha
            self._obter_engradados_recursivo(i + 1, 0, engradados_encontrados)
            return

        # Adiciona os engradados da pilha atual
        for engradado in self.matriz[i][j].engradados:
            engradados_encontrados.append(engradado)
        
        # Chama recursivamente para a próxima coluna
        self._obter_engradados_recursivo(i, j + 1, engradados_encontrados)

    def obter_todos_engradados(self):
        """Retorna uma lista com todos os engradados no estoque (usando recursividade)."""
        todos_engradados = []
        self._obter_engradados_recursivo(0, 0, todos_engradados)
        return todos_engradados

    def obter_produtos_proximos_vencimento(self, produtos_cadastrados, dias=30):
        """
        Retorna uma lista de produtos (e suas quantidades) próximos ao vencimento.
        Usa os engradados do estoque e a data de validade do produto.
        """
        produtos_vencendo = []
        data_limite = datetime.now() + timedelta(days=dias)
        
        engradados_no_estoque = self.obter_todos_engradados() # Usa a função recursiva

        for engradado in engradados_no_estoque:
            for produto_info in produtos_cadastrados:
                if produto_info.codigo == engradado.produto_codigo:
                    if produto_info.data_validade <= data_limite:
                        produtos_vencendo.append({
                            'codigo': produto_info.codigo,
                            'nome': produto_info.nome,
                            'lote': produto_info.lote,
                            'quantidade_engradado': engradado.quantidade,
                            'data_validade': produto_info.data_validade.strftime("%Y-%m-%d")
                        })
                    break # Encontrou o produto, pode sair do loop interno
        return produtos_vencendo

    def obter_itens_em_falta(self, produtos_cadastrados, limite_baixo=10):
        """
        Retorna uma lista de produtos (e suas quantidades em falta) com estoque abaixo de um limite.
        """
        itens_em_falta = []
        for produto in produtos_cadastrados:
            total_em_estoque = self.contar_por_produto(produto.codigo)
            if total_em_estoque < limite_baixo:
                itens_em_falta.append({
                    'codigo': produto.codigo,
                    'nome': produto.nome,
                    'total_em_estoque': total_em_estoque,
                    'limite_baixo': limite_baixo,
                    'faltando': limite_baixo - total_em_estoque
                })
        return itens_em_falta