from py2neo import Graph, Node, Relationship
from vendedor import listarEmailsVendedores

graph = Graph("neo4j+ssc://16df7b0f.databases.neo4j.io", auth=("neo4j", "v4MKtvAydl1gg6a9yuXTcYJGToPJ_rJVVNs0O8fZ6Hw"))
def menuProduto():
    print("\nPRODUTOS")
    print("Escolha uma ação \n")
    print(" 1 - Adicionar produto \n 2 - Visualizar todos produtos \n 3 - Visualizar produto \n 4 - Atualizar produto \n 5 - Deletar produto \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0, 1, 2, 3, 4, 5]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))
    if acao == 1:
        print("\nCADASTRO")
        listarEmailsVendedores()
        email = input("Digite o email do vendedor do produto que deseja cadastrar: ")
        inserirProduto(email)
        print(f'Produto cadastrado com sucesso!')
    elif acao == 2:
        print("\nPRODUTOS")
        produtos = visualizarProdutos()
        for produto in produtos:
            print(f"\nNome: {produto['nome']} \nPreço: R$ {produto['preco']} \nQuantidade: {produto['quantidade']} \nVendedor: {produto['nome_vendedor']}")
    elif acao == 3:
        print("\nPRODUTOS:")
        listarNomesProdutos()
        nome = input("\nDigite o nome do produto que deseja visualizar: ")
        lista = visualizarProduto(nome)
        print("\nPRODUTO ESCOLHIDO")
        for produtoObj in lista:
            for produto in produtoObj:
                print(f"\nNome: {produto['nome']} \nPreço: R$ {produto['preco']} \nQuantidade: {produto['quantidade']}")
    elif acao == 4:
        print("\nATUALIZAR \nPRODUTOS:")
        listarNomesProdutos()
        nome = input("\nDigite o nome do produto que deseja atualizar: ")
        atualizarProduto(nome)
        print(f'\nProduto atualizado com sucesso!')
    elif acao == 5:
        print("\nDELETAR")
        print("\nPRODUTOS:")
        listarNomesProdutos()
        nome = input("\nDigite o nome do produto que deseja deletar: ")
        deletarProduto(nome)
        print(f'\nProduto deletado com sucesso!')

    if acao != 0:
        menuProduto()


def listarNomesProdutos():
    result = graph.run("MATCH (p:Produto) RETURN p.nome AS nome")
    for record in result:
        print(record["nome"])


def inserirProduto(email):
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preço (XX.XX): R$ "))
    quantidade = input("Digite a quantidade do produto: ")
    query = '''MATCH (v:Vendedor) WHERE v.email = $email CREATE (p:Produto {nome: $nome, preco: $preco, quantidade: $quantidade})
    CREATE (p)-[:VENDIDO_POR]->(v) RETURN p'''
    graph.run(query, email=email, nome=nome, preco=preco, quantidade=quantidade)


def visualizarProdutos():
    query = '''MATCH (p:Produto)-[:VENDIDO_POR]->(v:Vendedor) RETURN p.nome AS nome, p.quantidade AS quantidade, p.preco AS preco, v.nome AS nome_vendedor,
    v.email AS email_vendedor, v.cpf AS cpf_vendedor'''
    result = graph.run(query)
    return result.data()        


def visualizarProduto(nome):
    result = graph.run("MATCH (p:Produto {nome: $nome}) RETURN p", nome=nome)
    found_users = list(result)
    return found_users

def atualizarProduto(nome):
    novosValores = {}
    desejo = input("Deseja atualizar o nome? S/N ")
    if desejo == "S":
        novoNome = input("Digite o novo nome do produto: ")
        novosValores["nome"] = novoNome
    desejo = input("Deseja atualizar o preço? S/N ")
    if desejo == "S":
        novoPreco = float(input("Digite o novo preço do produto (XX.XX): R$"))
        novosValores["preco"] = novoPreco
    desejo = input("Deseja atualizar a quantidade em estoque? S/N ")
    if desejo == "S":
        novaQuantidade = int(input("Digite a nova quantidade: "))
        novosValores["quant_produto"] = novaQuantidade

    graph.run("MATCH (p:Produto {nome: $nome}) SET p += $novosValores", nome=nome, novosValores=novosValores)


def deletarProduto(nome):
    query = ("MATCH (p:Produto) WHERE p.nome = $nome DETACH DELETE p")
    graph.run(query, nome=nome)
