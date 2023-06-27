from py2neo import Graph, Node, Relationship

graph = Graph("neo4j+ssc://16df7b0f.databases.neo4j.io", auth=("neo4j", "v4MKtvAydl1gg6a9yuXTcYJGToPJ_rJVVNs0O8fZ6Hw"))

def menuVendedor():
    print("\nVENDEDORES")
    print("Escolha uma ação \n")
    print(" 1 - Adicionar vendedor \n 2 - Visualizar todos vendedores \n 3 - Visualizar vendedor \n 4 - Atualizar vendedor \n 5 - Deletar vendedor \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0,1,2,3,4,5]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))

    if acao == 1:
        print("\nCADASTRO")
        inserirVendedor()
        print(f'\nVendedor cadastrado com sucesso!')
    elif acao == 2:
        print("\nVENDEDORES")
        vendedores = visualizarVendedores()
        for vendedor in vendedores:
            print(f"\nNome: {vendedor['nome']} \nEmail: {vendedor['email']} \nCPF: {vendedor['cpf']}")
    elif acao == 3:
        print("\nEMAILS VENDEDORES:")
        listarEmailsVendedores()
        email = input("\nDigite o email do vendedor que deseja visualizar: ")
        lista = visualizarVendedor(email)
        print("\nVENDEDOR ESCOLHIDO")
        for vendedorObj in lista:
            for vendedor in vendedorObj:
                print(f"\nNome: {vendedor['nome']} \nEmail: {vendedor['email']} \nCPF: {vendedor['cpf']}")
    elif acao == 4:
        print("\nATUALIZAR \nEMAILS VENDEDORES:")
        listarEmailsVendedores()
        email = input("Digite o email do vendedor que deseja atualizar: ")
        atualizarVendedor(email)
        print('\nVendedor atualizado com sucesso!')
    elif  acao == 5:
        print("\nDELETAR")
        print("EMAILS VENDEDORES:")
        listarEmailsVendedores()
        email = input("\nDigite o email do vendedor que deseja deletar: ")
        deletarVendedor(email)
        print(f'\nVendedor deletado com sucesso!')
    
    if acao != 0:
        menuVendedor()


def listarEmailsVendedores():
    result = graph.run("MATCH (v:Vendedor) RETURN v.email")
    emails = [record["v.email"] for record in result]
    for email in emails:
        print(email)


def inserirVendedor():
    nome = input("Digite o nome completo do vendedor: ")
    email = input("Digite o email: ")
    cpf = input("Digite o CPF: ")
    graph.create(Node("Vendedor", nome=nome, email=email, cpf=cpf))

def visualizarVendedores():
    result = graph.run("MATCH (v:Vendedor) RETURN v.nome AS nome, v.email AS email, v.cpf AS cpf")
    return  result.data()


def visualizarVendedor(email):
    result = graph.run("MATCH (v:Vendedor {email: $email}) RETURN v", email=email)
    found_users = list(result)
    return found_users


def atualizarVendedor(email):
    novosValores = {}
    desejo = input("Deseja atualizar o nome? S/N ")
    if desejo == "S":
        novoNome = input("\nDigite o novo nome do vendedor: ")
        novosValores["nome"] = novoNome
    desejo = input("Deseja atualizar o email? S/N ")
    if desejo == "S":
        novoEmail = input("Digite o novo email: ")
        novosValores["email"] = novoEmail
    desejo = input("Deseja atualizar o CPF? S/N ")
    if desejo == "S":
        novoCpf = input("Digite o novo CPF: ")
        novosValores["cpf"] = novoCpf
    graph.run("MATCH (v:Vendedor {email: $email}) SET v += $novosValores", email=email, novosValores=novosValores)

def deletarVendedor(email):  
    query = ("MATCH (v:Vendedor) WHERE v.email = $email DETACH DELETE v")
    graph.run(query, email=email)

