# Importa datetime para manipular datas de validade e fabricação.
# Importa json para serializar e desserializar os dados dos produtos para/de arquivos.
from datetime import datetime
import json

# A classe Produto define a estrutura de dados para cada item cadastrado no sistema.
# Contém todas as informações relevantes de um produto.
class Produto:
    """
    Representa um produto com todos os seus atributos.
    """
    def __init__(self , codigo , lote , nome , peso , data_validade , data_fabricacao , preco_compra , preco_venda , fornecedor , fabricante , categoria, capacidade_engradado=None):
        """
        Inicializa um novo objeto Produto.

        Args:
            Todos os atributos do produto, como código, nome, datas, etc.
            capacidade_engradado (int, opcional): Define o máximo de itens que um engradado
                                                  deste produto pode conter.
        """
        self.codigo = codigo
        self.lote = lote
        self.nome = nome 
        self.peso = peso
        # Converte as strings de data (formato "YYYY-MM-DD") para objetos datetime.
        self.data_validade = datetime.strptime(data_validade , "%Y-%m-%d")
        self.data_fabricacao = datetime.strptime(data_fabricacao , "%Y-%m-%d")
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.fornecedor = fornecedor
        self.fabricante = fabricante
        self.categoria = categoria
        # Atributo para definir a capacidade máxima de um engradado para este produto.
        self.capacidade_engradado = capacidade_engradado 
        
    def para_dicionario(self):
        """
        Converte o objeto Produto em um dicionário.
        Isso é útil para salvar os dados em formato JSON.
        As datas são convertidas de volta para strings.

        Returns:
            dict: Um dicionário com os atributos do produto.
        """
        return {
            'codigo': self.codigo, 
            'lote': self.lote,
            'nome': self.nome,
            'peso': self.peso,
            'data_validade': self.data_validade.strftime("%Y-%m-%d"),
            'data_fabricacao': self.data_fabricacao.strftime("%Y-%m-%d"),
            'preco_compra': self.preco_compra,
            'preco_venda': self.preco_venda,
            'fornecedor': self.fornecedor,
            'fabricante': self.fabricante,
            'categoria': self.categoria,
            'capacidade_engradado': self.capacidade_engradado
        }

def salvar_produtos(lista_produtos, nome_arquivo):
    """
    Salva uma lista de objetos Produto em um arquivo JSON.

    Args:
        lista_produtos (list): A lista de objetos Produto a ser salva.
        nome_arquivo (str): O caminho do arquivo onde os dados serão salvos.
    """
    # Usa uma list comprehension para converter cada objeto Produto em um dicionário.
    lista_dict = [produto.para_dicionario() for produto in lista_produtos]
    # Abre o arquivo em modo de escrita ('w') e salva a lista de dicionários.
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        # json.dump serializa o objeto Python para o formato JSON.
        # indent=4 formata o JSON para ser mais legível.
        json.dump(lista_dict, f, ensure_ascii=False, indent=4)

def carregar_produtos(nome_arquivo):
    """
    Carrega produtos de um arquivo JSON e os converte em uma lista de objetos Produto.

    Args:
        nome_arquivo (str): O caminho do arquivo de onde os dados serão carregados.

    Returns:
        list: Uma lista de objetos Produto.
    """
    lista_produtos = []
    try:
        # Abre o arquivo em modo de leitura ('r').
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            # Carrega os dados do arquivo JSON para uma lista de dicionários.
            lista_dict = json.load(f)
            # Itera sobre cada dicionário na lista.
            for d in lista_dict:
                # .get() é usado para carregar o novo atributo 'capacidade_engradado'.
                # Isso garante compatibilidade com arquivos antigos que não possuem esse campo.
                capacidade = d.get('capacidade_engradado') 
                # Cria um objeto Produto a partir do dicionário.
                produto = Produto(
                    d['codigo'], d['lote'], d['nome'], d['peso'], d['data_validade'],
                    d['data_fabricacao'], d['preco_compra'], d['preco_venda'],
                    d['fornecedor'], d['fabricante'], d['categoria'],
                    capacidade_engradado=capacidade
                )
                lista_produtos.append(produto)
    # Se o arquivo não for encontrado, o programa continua com uma lista vazia.
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado. Criando novo arquivo.")
    # Retorna a lista de produtos (pode estar vazia se o arquivo não existia).
    return lista_produtos