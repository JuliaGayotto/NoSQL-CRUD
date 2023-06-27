from usuario import visualizarUsuario, listarEmailsUsuarios
from produto import visualizarProduto, listarNomesProdutos, visualizarProdutos
from py2neo import Graph, Node, Relationship

graph = Graph("neo4j+ssc://16df7b0f.databases.neo4j.io", auth=("neo4j", "v4MKtvAydl1gg6a9yuXTcYJGToPJ_rJVVNs0O8fZ6Hw"))

def menuCompra():
    print("\nCOMPRAS")
    print("Escolha uma ação \n")
    print(" 1 - Adicionar compra \n 2 - Visualizar todas as compras \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma ação: "))
    opcoes = [0, 1, 2, 3, 4]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))

    if acao == 1:
        print("\nCADASTRO")
        inserirCompra()
        print(f'\nCompra cadastrada com sucesso!')
    elif acao == 2:
        print("\nCOMPRAS")
        compras = visualizarCompras()
        for compra in compras:
            selecionarCompra(compra)

    if acao != 0:
        menuCompra()


def selecionarCompra(compra):
    print(f"\nUsuário:  Nome: {compra['nome']}  Email: {compra['email']}  CPF: {compra['cpf']}")
    produtos = compra['produtos']
    for produto in produtos:
        print(f"Produto:  \nNome: {produto['nome']}\nPreço: {produto['preco']}\nQuantidade comprada: {produto['quantidade']}")


def inserirCompra():
    print("EMAIL USUÁRIOS:")
    listarEmailsUsuarios()
    email = input("Digite o email do usuário: ")
    produtos = []
    desejo = 'S'
    print("PRODUTOS")
    listarNomesProdutos()
    while desejo == 'S':
        nome= input("Digite o nome do produto: ")
        result = graph.run("MATCH (u:Produto {nome: $nome}) RETURN ID(u) AS idProduto", nome=nome)
        idProduto = result.evaluate("idProduto")
        produtos.append(idProduto)
        desejo = input("Deseja adicionar outro produto? S/N ")
    graph.run("MATCH (u:Usuario {email: $email}) UNWIND $produtos AS produto MATCH (p:Produto) WHERE ID(p) = produto CREATE (u)-[:FEZ_COMPRA]->(c:Compra)-[:CONTEM]->(p)", email=email, produtos=produtos)


def visualizarCompras():
    result = graph.run("MATCH (u:Usuario)-[:FEZ_COMPRA]->(c:Compra)-[:CONTEM]->(p:Produto) RETURN u.nome AS nome, u.cpf AS cpf, u.email AS email, COLLECT(p) AS produtos")
    return result.data()
