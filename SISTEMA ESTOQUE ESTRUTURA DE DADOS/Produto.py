from datetime import datetime
import json

class Produto:
    def __init__(self , codigo , lote , nome , peso , data_validade , data_fabricacao , preco_compra , preco_venda , fornecedor , fabricante , categoria, capacidade_engradado=None):
        self.codigo = codigo
        self.lote = lote
        self.nome = nome 
        self.peso = peso
        self.data_validade = datetime.strptime(data_validade , "%Y-%m-%d")
        self.data_fabricacao = datetime.strptime(data_fabricacao , "%Y-%m-%d")
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.fornecedor = fornecedor
        self.fabricante = fabricante
        self.categoria = categoria
        self.capacidade_engradado = capacidade_engradado # Novo atributo
        
    def para_dicionario(self):
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
            'capacidade_engradado': self.capacidade_engradado # Adiciona ao dicionário
        }

def salvar_produtos(lista_produtos, nome_arquivo):
    lista_dict = [produto.para_dicionario() for produto in lista_produtos]
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(lista_dict, f, ensure_ascii=False, indent=4)

def carregar_produtos(nome_arquivo):
    lista_produtos = []
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            lista_dict = json.load(f)
            for d in lista_dict:
                # Carrega o novo atributo, com um valor padrão se não existir (para compatibilidade com arquivos antigos)
                capacidade = d.get('capacidade_engradado') 
                produto = Produto(
                    d['codigo'],
                    d['lote'],
                    d['nome'],
                    d['peso'],
                    d['data_validade'],
                    d['data_fabricacao'],
                    d['preco_compra'],
                    d['preco_venda'],
                    d['fornecedor'],
                    d['fabricante'],
                    d['categoria'],
                    capacidade_engradado=capacidade # Passa o novo atributo
                )
                lista_produtos.append(produto)
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado. Criando novo arquivo.")
    return lista_produtos