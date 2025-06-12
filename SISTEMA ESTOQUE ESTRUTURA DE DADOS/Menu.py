import json
import os  # <- IMPORTANTE: Adicionar a biblioteca OS
from Produto import Produto, carregar_produtos, salvar_produtos
from Engradado import Engradado
from Estoque import Estoque
from Fila_de_Pedidos import FilaPedidos
from Pedido import Pedido

# --- CONSTRUÇÃO DINÂMICA E SEGURA DO CAMINHO PARA OS ARQUIVOS ---

# Pega o caminho absoluto da pasta onde este script (Menu.py) está localizado
CAMINHO_BASE = os.path.dirname(os.path.abspath(__file__))

# Combina o caminho base com o nome de cada arquivo JSON
# Isso garante que o Python sempre encontrará os arquivos, não importa de onde você execute o projeto.
ARQUIVO_PRODUTOS = os.path.join(CAMINHO_BASE, 'produtos.json')
ARQUIVO_ESTOQUE = os.path.join(CAMINHO_BASE, 'estoque.json')
ARQUIVO_PEDIDOS = os.path.join(CAMINHO_BASE, 'pedidos.json')


# --- Inicialização do Sistema ---
print("--- Carregando Sistema de Estoque ---")
# Carrega os produtos existentes do arquivo JSON
produtos_cadastrados = carregar_produtos(ARQUIVO_PRODUTOS)

# Cria uma instância do Estoque e carrega os dados
estoque = Estoque()
estoque.carregar_estoque(ARQUIVO_ESTOQUE)

# Cria uma instância da Fila de Pedidos e carrega os dados
fila_pedidos = FilaPedidos()
fila_pedidos.carregar_pedidos(ARQUIVO_PEDIDOS)
print("--- Sistema Carregado com Sucesso ---\n")

# --- Funções do Menu (as funções como cadastrar_novo_produto, etc., continuam as mesmas) ---

def cadastrar_novo_produto():
    # (Seu código original aqui)
    print("\n--- Cadastro de Novo Produto ---")
    codigo = input("Código: ")
    
    if any(p.codigo == codigo for p in produtos_cadastrados):
        print("Erro: Já existe um produto com este código.")
        return

    lote = input("Lote: ")
    nome = input("Nome: ")
    peso = float(input("Peso: "))
    data_validade = input("Data de validade (YYYY-MM-DD): ")
    data_fabricacao = input("Data de fabricação (YYYY-MM-DD): ")
    preco_compra = float(input("Preço de compra: "))
    preco_venda = float(input("Preço de venda: "))
    fornecedor = input("Fornecedor: ")
    fabricante = input("Fabricante: ")
    categoria = input("Categoria: ")

    novo_produto = Produto(
        codigo, lote, nome, peso, data_validade, data_fabricacao,
        preco_compra, preco_venda, fornecedor, fabricante, categoria
    )
    produtos_cadastrados.append(novo_produto)
    print(f"\nProduto '{nome}' cadastrado com sucesso!")


def adicionar_engradado_estoque():
    # (Seu código original aqui)
    print("\n--- Adicionar Engradado ao Estoque ---")
    codigo_produto = input("Código do produto: ")

    if not any(p.codigo == codigo_produto for p in produtos_cadastrados):
        print("Erro: Nenhum produto encontrado com este código. Cadastre o produto primeiro.")
        return
        
    try:
        quantidade = int(input("Quantidade de itens no engradado: "))
        if quantidade <= 0:
            print("A quantidade deve ser um número positivo.")
            return
    except ValueError:
        print("Erro: Quantidade inválida.")
        return

    engradado = Engradado(codigo_produto, quantidade)

    if estoque.adicionar_engradado(engradado):
        print("\nEngradado adicionado ao estoque com sucesso.")
    else:
        print("\nErro: Estoque cheio ou nenhuma pilha compatível encontrada.")


def remover_unidades_estoque():
    # (Seu código original aqui)
    print("\n--- Remover Unidades do Estoque ---")
    codigo = input("Código do produto para remover: ")
    
    try:
        quantidade = int(input("Quantidade a remover: "))
        if quantidade <= 0:
            print("A quantidade deve ser um número positivo.")
            return
    except ValueError:
        print("Erro: Quantidade inválida.")
        return

    engradados_removidos = estoque.remover_engradado(codigo, quantidade)

    if engradados_removidos is not None:
        print(f"\nRemoção concluída com sucesso.")
    else:
        print("\nNão foi possível remover a quantidade desejada (estoque insuficiente ou produto não encontrado).")


def visualizar_estoque():
    # (Seu código original aqui)
    print("\n--- Visualização do Estoque ---")
    estoque.visualizar()


def registrar_pedido():
    # (Seu código original aqui)
    print("\n--- Registrar Novo Pedido ---")
    codigo_produto = input("Código do produto: ")
    
    if not any(p.codigo == codigo_produto for p in produtos_cadastrados):
        print("Erro: Nenhum produto encontrado com este código.")
        return

    try:
        quantidade = int(input("Quantidade desejada: "))
        if quantidade <= 0:
            print("A quantidade deve ser um número positivo.")
            return
    except ValueError:
        print("Erro: Quantidade inválida.")
        return
        
    data_solicitacao = input("Data da solicitação (YYYY-MM-DD): ")
    solicitante = input("Nome do solicitante: ")

    try:
        pedido = Pedido(codigo_produto, quantidade, data_solicitacao, solicitante)
        fila_pedidos.adicionar_pedido(pedido)
        print("\nPedido registrado com sucesso.")
    except ValueError as e:
        print(f"Erro ao registrar o pedido: {e}. Verifique o formato da data.")


def processar_pedidos():
    # (Seu código original aqui)
    print("\n--- Processando Pedido ---")
    if not fila_pedidos.fila:
        print("Não há pedidos na fila para processar.")
        return
    
    fila_pedidos.processar_pedido(estoque)


def gerar_relatorios():
    # (Seu código original aqui)
    print("\n--- Relatório de Estoque por Produto ---")
    if not produtos_cadastrados:
        print("Nenhum produto cadastrado.")
        return
        
    for produto in produtos_cadastrados:
        total_unidades = estoque.contar_por_produto(produto.codigo)
        print(f"Produto: {produto.nome} (Cód: {produto.codigo}) - Total em Estoque: {total_unidades} unidades")

def salvar_tudo():
    """Salva o estado de todos os dados do sistema (produtos, estoque, pedidos)."""
    salvar_produtos(produtos_cadastrados, ARQUIVO_PRODUTOS)
    estoque.salvar_estoque(ARQUIVO_ESTOQUE)
    fila_pedidos.salvar_pedidos(ARQUIVO_PEDIDOS)
    print("\nTodos os dados foram salvos com sucesso!")

def menu():
    """Função principal que exibe o menu e gerencia as opções."""
    while True:
        print("\n=========== MENU DO SISTEMA DE ESTOQUE ===========")
        print("1. Cadastrar Novo Produto")
        print("2. Adicionar Engradado ao Estoque")
        print("3. Remover Unidades do Estoque")
        print("4. Visualizar Estoque")
        print("5. Registrar Pedido de Cliente")
        print("6. Processar Próximo Pedido da Fila")
        print("7. Gerar Relatório de Estoque")
        print("8. Salvar Tudo")
        print("0. Sair")
        print("==================================================")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_novo_produto()
        elif opcao == '2':
            adicionar_engradado_estoque()
        elif opcao == '3':
            remover_unidades_estoque()
        elif opcao == '4':
            visualizar_estoque()
        elif opcao == '5':
            registrar_pedido()
        elif opcao == '6':
            processar_pedidos()
        elif opcao == '7':
            gerar_relatorios()
        elif opcao == '8':
            salvar_tudo()
        elif opcao == '0':
            salvar_tudo()
            print("\nAlterações salvas. Saindo do sistema...")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()