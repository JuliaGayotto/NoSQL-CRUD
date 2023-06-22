from neo4j import GraphDatabase
from vendedor import visualizarVendedor, listarEmailsVendedores, adicionarProdutosVendedor

driver = neo4j.GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

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
            print(f"\nNome: {produto['nome']} \nPreço: {produto['preco']} \nQuantidade: {produto['quant_produto']} \nVendedor: {produto['vendedor']['nome_vendedor']}")
    elif acao == 3:
        print("\nPRODUTOS:")
        listarNomesProdutos()
        nome = input("\nDigite o nome do produto que deseja visualizar: ")
        produto = visualizarProduto(nome)
        print("\nPRODUTO ESCOLHIDO")
        print(f"\nNome: {produto['nome']} \nPreço: {produto['preco']} \nQuantidade: {produto['quant_produto']}")
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
    with driver.session() as session:
        query = "MATCH (p:Produto) RETURN p.nome AS nome"
        result = session.run(query)
        for record in result:
        print(record["nome"])



def inserirProduto(email):
    with driver.session() as session:
        vend = visualizarVendedor(email)
        vendedor = {"id": vend.get('_id'), "nome_vendedor": vend.get('nome_vendedor'), "email": vend.get('email'), "cpf": vend.get('cpf')}
        nome = input("Digite o nome do produto: ")
        preco = float(input("Digite o preço (XX.XX): R$ "))
        quant_produto = int(input("Digite a quantidade do produto: "))
        query = '''
        MATCH (v:Vendedor)
        WHERE v.email = $email
        CREATE (p:Produto {nome: $nome, preco: $preco, quant_produto: $quant_produto})
        CREATE (p)-[:PERTENCE_A]->(v)
        RETURN p
        '''
        result = session.run(query, email=email, nome=nome, preco=preco, quant_produto=quant_produto)
        return result.single()[0]

def visualizarProdutos():
    with driver.session() as session:
        query = '''
        MATCH (p:Produto)-[:PERTENCE_A]->(v:Vendedor)
        RETURN p, v
        '''
        result = session.run(query)
        return result.records()

def visualizarProduto(nome):
    with driver.session() as session:
        query = '''
        MATCH (p:Produto {nome: $nome})-[:PERTENCE_A]->(v:Vendedor)
        RETURN p, v
        '''
        result = session.run(query, nome=nome)
        return result.single()

def atualizarProduto(nome):
    with driver.session() as session:
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
        query = '''
        MATCH (p:Produto {nome: $nome})
        SET p += $novosValores
        RETURN p
        '''
        result = session.run(query, nome=nome, novosValores=novosValores)
        return result.single()

def deletarProduto(nome):
    with driver.session() as session:
        query = '''
        MATCH (p:Produto {nome: $nome})
        DELETE p
        '''
        session.run(query, nome=nome)