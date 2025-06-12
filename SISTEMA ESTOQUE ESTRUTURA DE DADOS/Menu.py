import json
import os
from Produto import Produto, carregar_produtos, salvar_produtos
from Engradado import Engradado
from Estoque import Estoque
from Fila_de_Pedidos import FilaPedidos
from Pedido import Pedido
from datetime import datetime, timedelta

# --- CONSTRUÇÃO DINÂMICA E SEGURA DO CAMINHO PARA OS ARQUIVOS ---

CAMINHO_BASE = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_PRODUTOS = os.path.join(CAMINHO_BASE, 'produtos.json')
ARQUIVO_ESTOQUE = os.path.join(CAMINHO_BASE, 'estoque.json')
ARQUIVO_PEDIDOS = os.path.join(CAMINHO_BASE, 'pedidos.json')


# --- Inicialização do Sistema ---
print("--- Carregando Sistema de Estoque ---")
produtos_cadastrados = carregar_produtos(ARQUIVO_PRODUTOS)
estoque = Estoque()
estoque.carregar_estoque(ARQUIVO_ESTOQUE)
fila_pedidos = FilaPedidos()
fila_pedidos.carregar_pedidos(ARQUIVO_PEDIDOS)
print("--- Sistema Carregado com Sucesso ---\n")

# --- Funções do Menu ---

def cadastrar_novo_produto():
    print("\n--- Cadastro de Novo Produto ---")
    codigo = input("Código: ")
    
    if any(p.codigo == codigo for p in produtos_cadastrados):
        print("Erro: Já existe um produto com este código.")
        return

    lote = input("Lote: ")
    nome = input("Nome: ")
    
    try:
        peso = float(input("Peso: "))
        capacidade_engradado_str = input("Capacidade máxima de unidades por engradado para este produto (deixe em branco para ilimitado): ")
        if capacidade_engradado_str == "":
            capacidade_engradado = None
        else:
            capacidade_engradado = int(capacidade_engradado_str)
            if capacidade_engradado <= 0:
                print("A capacidade do engradado deve ser um número positivo ou deixada em branco.")
                return
    except ValueError:
        print("Erro: Peso ou capacidade do engradado inválido.")
        return

    data_validade = input("Data de validade (YYYY-MM-DD): ")
    data_fabricacao = input("Data de fabricação (YYYY-MM-DD): ")
    
    try:
        preco_compra = float(input("Preço de compra: "))
        preco_venda = float(input("Preço de venda: "))
    except ValueError:
        print("Erro: Preço de compra ou venda inválido.")
        return

    fornecedor = input("Fornecedor: ")
    fabricante = input("Fabricante: ")
    categoria = input("Categoria: ")

    novo_produto = Produto(
        codigo, lote, nome, peso, data_validade, data_fabricacao,
        preco_compra, preco_venda, fornecedor, fabricante, categoria,
        capacidade_engradado=capacidade_engradado
    )
    produtos_cadastrados.append(novo_produto)
    print(f"\nProduto '{nome}' cadastrado com sucesso!")


def adicionar_engradado_estoque():
    print("\n--- Adicionar Engradado ao Estoque ---")
    codigo_produto = input("Código do produto: ")

    produto_encontrado = None
    for p in produtos_cadastrados:
        if p.codigo == codigo_produto:
            produto_encontrado = p
            break

    if not produto_encontrado:
        print("Erro: Nenhum produto encontrado com este código. Cadastre o produto primeiro.")
        return
        
    try:
        quantidade = int(input("Quantidade de itens no engradado: "))
        if quantidade <= 0:
            print("A quantidade deve ser um número positivo.")
            return
        if produto_encontrado.capacidade_engradado is not None and quantidade > produto_encontrado.capacidade_engradado:
            print(f"Erro: A quantidade ({quantidade}) excede a capacidade máxima de engradado para este produto ({produto_encontrado.capacidade_engradado}).")
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
    print("\n--- Remover Unidades do Estoque ---")
    codigo = input("Código do produto para remover: ")
    
    if not any(p.codigo == codigo for p in produtos_cadastrados):
        print("Erro: Nenhum produto encontrado com este código.")
        return

    try:
        quantidade = int(input("Quantidade a remover: "))
        if quantidade <= 0:
            print("A quantidade deve ser um número positivo.")
            return
    except ValueError:
        print("Erro: Quantidade inválida.")
        return
    
    total_disponivel = estoque.contar_por_produto(codigo)
    if total_disponivel < quantidade:
        print(f"Erro: Quantidade insuficiente em estoque. Disponível: {total_disponivel} unidades.")
        return

    remocao_sucesso = estoque.remover_engradado(codigo, quantidade)

    if remocao_sucesso:
        print(f"\nRemoção de {quantidade} unidades do produto {codigo} concluída com sucesso.")
    else:
        print("\nNão foi possível remover a quantidade desejada (estoque insuficiente ou produto não encontrado).")


def visualizar_estoque():
    print("\n--- Visualização do Estoque ---")
    estoque.visualizar()


def registrar_pedido():
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
    print("\n--- Processando Pedido ---")
    if not fila_pedidos.fila:
        print("Não há pedidos na fila para processar.")
        return
    
    fila_pedidos.processar_pedido(estoque)


def gerar_relatorio_estoque_geral(): # Renomeada para clareza
    print("\n--- Relatório de Estoque por Produto (Geral) ---")
    if not produtos_cadastrados:
        print("Nenhum produto cadastrado.")
        return
        
    for produto in produtos_cadastrados:
        total_unidades = estoque.contar_por_produto(produto.codigo)
        print(f"Produto: {produto.nome} (Cód: {produto.codigo}) - Total em Estoque: {total_unidades} unidades")


def gerar_relatorio_vencimento():
    print("\n--- Relatório de Produtos Próximos ao Vencimento (Próximos 30 dias) ---")
    produtos_vencendo = estoque.obter_produtos_proximos_vencimento(produtos_cadastrados)
    
    if not produtos_vencendo:
        print("Nenhum produto próximo ao vencimento nos próximos 30 dias.")
        return

    for item in produtos_vencendo:
        print(f"  Produto: {item['nome']} (Cód: {item['codigo']}), Lote: {item['lote']}, Quantidade no engradado: {item['quantidade_engradado']}, Vencimento: {item['data_validade']}")

def gerar_relatorio_itens_em_falta():
    print("\n--- Relatório de Itens em Falta (Estoque abaixo de 10 unidades) ---")
    itens_em_falta = estoque.obter_itens_em_falta(produtos_cadastrados)

    if not itens_em_falta:
        print("Nenhum item em falta (todos com estoque acima de 10 unidades).")
        return

    for item in itens_em_falta:
        print(f"  Produto: {item['nome']} (Cód: {item['codigo']}) - Em Estoque: {item['total_em_estoque']} unidades, Faltam para o limite ({item['limite_baixo']}): {item['faltando']} unidades.")

def gerar_historico_pedidos_atendidos():
    print("\n--- Histórico de Pedidos Atendidos ---")
    historico = fila_pedidos.obter_historico_pedidos_atendidos()

    if not historico:
        print("Nenhum pedido foi atendido ainda.")
        return

    for pedido in historico:
        nome_produto = "Desconhecido"
        for p in produtos_cadastrados:
            if p.codigo == pedido.codigo_produto:
                nome_produto = p.nome
                break

        print(f"  Pedido de: {pedido.solicitante}, Produto: {nome_produto} (Cód: {pedido.codigo_produto}), Quantidade: {pedido.quantidade}, Data: {pedido.data_solicitacao.strftime('%Y-%m-%d')}")

# --- NOVA FUNÇÃO PARA JUNTAR TODOS OS RELATÓRIOS ---
def gerar_todos_relatorios():
    print("\n=========== GERANDO TODOS OS RELATÓRIOS ===========")
    gerar_relatorio_estoque_geral()
    print("\n---------------------------------------------------")
    gerar_relatorio_vencimento()
    print("\n---------------------------------------------------")
    gerar_relatorio_itens_em_falta()
    print("\n---------------------------------------------------")
    gerar_historico_pedidos_atendidos()
    print("\n================= FIM DOS RELATÓRIOS ================\n")


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
        print("7. Gerar Todos os Relatórios") # Opção 7 agora chama a nova função
        print("8. Salvar Tudo") # Reajustado para 8
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
        elif opcao == '7': # Chama a nova função que agrega os relatórios
            gerar_todos_relatorios()
        elif opcao == '8': # Opção para salvar tudo
            salvar_tudo()
        elif opcao == '0':
            salvar_tudo()
            print("\nAlterações salvas. Saindo do sistema...")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()