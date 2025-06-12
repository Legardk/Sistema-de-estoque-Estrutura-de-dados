import os
from Produto import carregar_produtos
from Estoque import Estoque
from Fila_de_Pedidos import FilaPedidos
import Operacoes_menu as op

CAMINHO_BASE = os.path.dirname(os.path.abspath(__file__))
ARQUIVOS_JSON = {
    "produtos": os.path.join(CAMINHO_BASE, 'produtos.json'),
    "estoque": os.path.join(CAMINHO_BASE, 'estoque.json'),
    "pedidos": os.path.join(CAMINHO_BASE, 'pedidos.json')
}

print("--- Carregando Sistema de Estoque ---")
produtos_cadastrados = carregar_produtos(ARQUIVOS_JSON['produtos'])
estoque = Estoque()
estoque.carregar_estoque(ARQUIVOS_JSON['estoque'])
fila_pedidos = FilaPedidos()
fila_pedidos.carregar_pedidos(ARQUIVOS_JSON['pedidos'])
print("--- Sistema Carregado com Sucesso ---\n")

def menu():
    """Função principal que exibe o menu e gerencia o loop de interação com o usuário."""
    # O loop `while True` mantém o programa em execução até que o usuário escolha sair.
    while True:
        print("\n=========== MENU DO SISTEMA DE ESTOQUE ===========")
        print("1. Cadastrar Novo Produto")
        print("2. Adicionar Engradado ao Estoque")
        print("3. Remover Unidades do Estoque")
        print("4. Visualizar Estoque")
        print("5. Registrar Pedido de Cliente")
        print("6. Processar Próximo Pedido da Fila")
        print("7. Gerar Todos os Relatórios")
        print("8. Salvar Tudo")
        print("0. Sair")
        print("==================================================")
        
        opcao = input("Escolha uma opção: ")

        # A estrutura if/elif/else direciona a execução para a função correta
        # no módulo 'operacoes_menu', passando os objetos de estado necessários.
        if opcao == '1':
            op.cadastrar_novo_produto(produtos_cadastrados)
        elif opcao == '2':
            op.adicionar_engradado_estoque(estoque, produtos_cadastrados)
        elif opcao == '3':
            op.remover_unidades_estoque(estoque, produtos_cadastrados)
        elif opcao == '4':
            op.visualizar_estoque(estoque)
        elif opcao == '5':
            op.registrar_pedido(fila_pedidos, produtos_cadastrados)
        elif opcao == '6':
            op.processar_pedidos(fila_pedidos, estoque)
        elif opcao == '7':
            op.gerar_todos_relatorios(estoque, fila_pedidos, produtos_cadastrados)
        elif opcao == '8':
            op.salvar_tudo(produtos_cadastrados, estoque, fila_pedidos, ARQUIVOS_JSON)
        elif opcao == '0':
            # Garante que todos os dados sejam salvos antes de encerrar.
            op.salvar_tudo(produtos_cadastrados, estoque, fila_pedidos, ARQUIVOS_JSON)
            print("\nAlterações salvas. Saindo do sistema...")
            break # Encerra o loop e o programa.
        else:
            print("\nOpção inválida! Tente novamente.")

# --- PONTO DE ENTRADA DO PROGRAMA ---
# A condição `if __name__ == "__main__":` garante que a função `menu()`
# só será chamada quando este arquivo for executado diretamente.
if __name__ == "__main__":
    menu()