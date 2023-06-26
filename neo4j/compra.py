from usuario import visualizarUsuario, listarEmailsUsuarios
from produto import visualizarProduto, listarNomesProdutos
from vendedor import visualizarVendedor, listarEmailsVendedores
from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j+ssc://16df7b0f.databases.neo4j.io", auth=("neo4j", "v4MKtvAydl1gg6a9yuXTcYJGToPJ_rJVVNs0O8fZ6Hw"))

def menuCompra():
    print("\nCOMPRAS")
    print("Escolha uma ação \n")
    print(" 1 - Adicionar compra \n 2 - Visualizar todas as compras \n 3 - Visualizar compra \n 4 - Deletar compra \n 0 - Voltar ao menu \n")
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
    elif acao == 3:
        id = input("Digite o ID da compra que deseja visualizar: ")
        compra = visualizarCompra(id)
        if compra:
            print("\nCOMPRA ESCOLHIDA")
            selecionarCompra(compra)
        else:
            print("Compra não encontrada.")
    elif acao == 4:
        print("\nDELETAR")
        id = input("Digite o ID da compra que deseja deletar: ")
        deletarCompra(id)
        print(f'\nCompra deletada com sucesso!')

    if acao != 0:
        menuCompra()


def selecionarCompra(compra):
    print(f"\nID da compra: {compra['id']}")
    print(f"Data da Compra: {compra['data_compra']}")
    usuario = compra['usuario']
    print(f"Usuário:  Nome: {usuario['nome']}  Email: {usuario['email']}  CPF: {usuario['cpf']}")
    vendedor = compra['vendedor']
    print(f"Vendedor:  Nome: {vendedor['nome_vendedor']}  Email: {vendedor['email']}  CPF: {vendedor['cpf']}")
    produtos = compra['produtos']
    for produto in produtos:
        print(f"Produto:  Nome: {produto['nome']}\nPreço: {produto['preco']}\nQuantidade comprada: {produto['quant_comprada']}")


def inserirCompra():
    with driver.session() as session:
        dataCompra = input("Digite a data da compra: ") 
        desejo = 'S'
        print("PRODUTOS")
        listarNomesProdutos()
        nomeProduto = input("Digite o nome do produto: ")
        prod = visualizarProduto(nomeProduto)
        preco =  prod['preco']   
        quant = input("Digite a quantidade comprada: ")
           

        print("EMAILS VENDEDORES:")
        listarEmailsVendedores()
        emailVendedor = input("Digite o email do vendedor: ")
        print("EMAIL USUÁRIOS:")
        listarEmailsUsuarios()
        emailUsuario = input("Digite o email do usuário: ")


        query = (
            "CREATE (c:Compra) WITH "
            "MATCH (u:Usuario {email: $emailUsuario}) "
            "MATCH (v:Vendedor {email: $emailVendedor}) "
            "MATCH (p:Produto {nome: $nomeProduto}) "
            "CREATE (u)-[:REALIZOU]->(c)"
            "CREATE (v)-[:VENDEU]->(c)"
            "CREATE (p)-[:ADQUIRIDO]->(c)"
        )

        session.run(query, emailUsuario=emailUsuario, emailVendedor=emailVendedor, nomeProduto=nomeProduto)


def visualizarCompras():
    with driver.session() as session:
        query = """
        MATCH (c:Compra)-[:COMPRA_USUARIO]->(u:Usuario)
        MATCH (c)-[:COMPRA_VENDEDOR]->(v:Vendedor)
        RETURN c, u, v
        """
        result = session.run(query)
        compras = []
        for record in result:
            compra = record['c']
            usuario = record['u']
            vendedor = record['v']
            compra['usuario'] = usuario
            compra['vendedor'] = vendedor
            compras.append(compra)
        return compras


def visualizarCompra(id):
    with driver.session() as session:
        query = """
        MATCH (c:Compra {id: $id})-[:COMPRA_USUARIO]->(u:Usuario)
        MATCH (c)-[:COMPRA_VENDEDOR]->(v:Vendedor)
        RETURN c, u, v
        """
        result = session.run(query, id=id)
        record = result.single()
        if record:
            compra = record['c']
            usuario = record['u']
            vendedor = record['v']
            compra['usuario'] = usuario
            compra['vendedor'] = vendedor
            return compra
        else:
            return None


def deletarCompra(id):
    with driver.session() as session:
        query = """
        MATCH (c:Compra {id: $id})
        DETACH DELETE c
        """
        session.run(query, id=id)
        return True
