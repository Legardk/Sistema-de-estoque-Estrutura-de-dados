from Produto import Produto, salvar_produtos
from Engradado import Engradado
from Pedido import Pedido

def cadastrar_novo_produto(produtos_cadastrados):
    """Lida com a lógica de coletar dados do usuário e criar um novo Produto."""
    print("\n--- Cadastro de Novo Produto ---")
    codigo = input("Código: ")
    
    if any(p.codigo == codigo for p in produtos_cadastrados):
        print("Erro: Já existe um produto com este código.")
        return

    lote = input("Lote: ")
    nome = input("Nome: ")
    
    try:
        peso = float(input("Peso: "))
        capacidade_engradado_str = input("Capacidade máxima de unidades por engradado (deixe em branco para ilimitado): ")
        capacidade_engradado = int(capacidade_engradado_str) if capacidade_engradado_str else None
        if capacidade_engradado is not None and capacidade_engradado <= 0:
            print("A capacidade do engradado deve ser um número positivo.")
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


def adicionar_engradado_estoque(estoque, produtos_cadastrados):
    """Coleta dados para criar um Engradado e adicioná-lo ao Estoque."""
    print("\n--- Adicionar Engradado ao Estoque ---")
    codigo_produto = input("Código do produto: ")

    produto_encontrado = next((p for p in produtos_cadastrados if p.codigo == codigo_produto), None)

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


def remover_unidades_estoque(estoque, produtos_cadastrados):
    """Remove uma quantidade específica de unidades de um produto do estoque."""
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

    if estoque.remover_engradado(codigo, quantidade):
        print(f"\nRemoção de {quantidade} unidades do produto {codigo} concluída com sucesso.")
    else:
        print("\nNão foi possível remover a quantidade desejada (estoque insuficiente ou produto não encontrado).")


def visualizar_estoque(estoque):
    """Chama o método de visualização do Estoque."""
    print("\n--- Visualização do Estoque ---")
    estoque.visualizar()


def registrar_pedido(fila_pedidos, produtos_cadastrados):
    """Coleta dados para criar um Pedido e adicioná-lo à Fila de Pedidos."""
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


def processar_pedidos(fila_pedidos, estoque):
    """Processa o próximo pedido da fila."""
    print("\n--- Processando Pedido ---")
    if not fila_pedidos.fila:
        print("Não há pedidos na fila para processar.")
        return
    
    fila_pedidos.processar_pedido(estoque)


def salvar_tudo(produtos_cadastrados, estoque, fila_pedidos, arquivos_json):
    """Salva o estado de todos os dados do sistema nos arquivos JSON."""
    salvar_produtos(produtos_cadastrados, arquivos_json['produtos'])
    estoque.salvar_estoque(arquivos_json['estoque'])
    fila_pedidos.salvar_pedidos(arquivos_json['pedidos'])
    print("\nTodos os dados foram salvos com sucesso!")


# --- Funções de Relatório ---

def gerar_relatorio_estoque_geral(estoque, produtos_cadastrados):
    """Exibe a quantidade total de cada produto cadastrado em estoque."""
    print("\n--- Relatório de Estoque por Produto (Geral) ---")
    if not produtos_cadastrados:
        print("Nenhum produto cadastrado.")
        return
        
    for produto in produtos_cadastrados:
        total_unidades = estoque.contar_por_produto(produto.codigo)
        print(f"Produto: {produto.nome} (Cód: {produto.codigo}) - Total em Estoque: {total_unidades} unidades")


def gerar_relatorio_vencimento(estoque, produtos_cadastrados):
    """Exibe os produtos em estoque que vencerão nos próximos 30 dias."""
    print("\n--- Relatório de Produtos Próximos ao Vencimento (Próximos 30 dias) ---")
    produtos_vencendo = estoque.obter_produtos_proximos_vencimento(produtos_cadastrados)
    
    if not produtos_vencendo:
        print("Nenhum produto próximo ao vencimento nos próximos 30 dias.")
        return

    for item in produtos_vencendo:
        print(f"  Produto: {item['nome']} (Cód: {item['codigo']}), Lote: {item['lote']}, Quantidade no engradado: {item['quantidade_engradado']}, Vencimento: {item['data_validade']}")

def gerar_relatorio_itens_em_falta(estoque, produtos_cadastrados):
    """Exibe produtos com estoque abaixo do limite mínimo (10 unidades)."""
    print("\n--- Relatório de Itens em Falta (Estoque abaixo de 10 unidades) ---")
    itens_em_falta = estoque.obter_itens_em_falta(produtos_cadastrados)

    if not itens_em_falta:
        print("Nenhum item em falta (todos com estoque acima de 10 unidades).")
        return

    for item in itens_em_falta:
        print(f"  Produto: {item['nome']} (Cód: {item['codigo']}) - Em Estoque: {item['total_em_estoque']} unidades, Faltam para o limite ({item['limite_baixo']}): {item['faltando']} unidades.")

def gerar_historico_pedidos_atendidos(fila_pedidos, produtos_cadastrados):
    """Exibe todos os pedidos que já foram processados com sucesso."""
    print("\n--- Histórico de Pedidos Atendidos ---")
    historico = fila_pedidos.obter_historico_pedidos_atendidos()

    if not historico:
        print("Nenhum pedido foi atendido ainda.")
        return

    for pedido in historico:
        nome_produto = next((p.nome for p in produtos_cadastrados if p.codigo == pedido.codigo_produto), "Desconhecido")
        print(f"  Pedido de: {pedido.solicitante}, Produto: {nome_produto} (Cód: {pedido.codigo_produto}), Quantidade: {pedido.quantidade}, Data: {pedido.data_solicitacao.strftime('%Y-%m-%d')}")


def gerar_todos_relatorios(estoque, fila_pedidos, produtos_cadastrados):
    """Função de conveniência que chama todas as funções de relatório de uma vez."""
    print("\n=========== GERANDO TODOS OS RELATÓRIOS ===========")
    gerar_relatorio_estoque_geral(estoque, produtos_cadastrados)
    print("\n---------------------------------------------------")
    gerar_relatorio_vencimento(estoque, produtos_cadastrados)
    print("\n---------------------------------------------------")
    gerar_relatorio_itens_em_falta(estoque, produtos_cadastrados)
    print("\n---------------------------------------------------")
    gerar_historico_pedidos_atendidos(fila_pedidos, produtos_cadastrados)
    print("\n================= FIM DOS RELATÓRIOS ================\n")