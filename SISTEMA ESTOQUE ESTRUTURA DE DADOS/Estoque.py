import json
from Pilha import Pilha
from Pedido import Pedido
from Engradado import Engradado

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
        retirados = []
        pilhas_modificadas = []
        quantidade_a_remover = quantidade

        # Itera sobre a matriz para encontrar os produtos
        for linha in self.matriz:
            for pilha in linha:
                if pilha.topo() and pilha.topo().produto_codigo == produto_codigo:
                    # Remove engradados da pilha atual enquanto necessário e possível
                    while pilha.topo() and quantidade_a_remover > 0:
                        removido = pilha.remover()
                        retirados.append(removido)
                        pilhas_modificadas.append((removido, pilha)) # Guarda o engradado e sua pilha original
                        quantidade_a_remover -= removido.quantidade
        
        if quantidade_a_remover <= 0:
            return retirados # Sucesso
        else:
            # Rollback em caso de falha (não encontrou a quantidade suficiente)
            for engradado, pilha_origem in reversed(pilhas_modificadas):
                pilha_origem.adicionar(engradado)
            return None

    def visualizar(self):
        for i, linha in enumerate(self.matriz):
            print(f"Linha {i}:")
            for j, pilha in enumerate(linha):
                topo = pilha.topo()
                if topo:
                    print(f"  Coluna {j}: {topo.produto_codigo} x {len(pilha.engradados)}")
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
                if not matriz_serializavel: return # Se o arquivo estiver vazio

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
            # Não é um erro, apenas informa que um novo arquivo será criado ao salvar
            pass
        except (json.JSONDecodeError, KeyError):
            print(f"Erro ao ler o arquivo de estoque '{nome_arquivo}'. Verifique o formato. Iniciando com estoque vazio.")