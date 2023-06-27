import json
from py2neo import Graph, Node, Relationship
from produto import visualizarProdutos, visualizarProduto, listarNomesProdutos

graph = Graph("neo4j+ssc://16df7b0f.databases.neo4j.io", auth=("neo4j", "v4MKtvAydl1gg6a9yuXTcYJGToPJ_rJVVNs0O8fZ6Hw"))

def menuUsuario():
    print("\n\nUSUÁRIOS")
    print("Escolha uma ação: \n")
    print(" 1 - Adicionar usuário \n 2 - Visualizar todos usuários \n 3 - Visualizar usuário \n 4 - Atualizar usuário \n 5 - Adicionar favoritos \n 6 - Deletar usuário \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma ação: "))
    opcoes = [0, 1, 2, 3, 4, 5, 6]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))

    if acao == 1:
        print("\nCADASTRO")
        inserirUsuario()
        print(f'\nUsuário cadastrado com sucesso!')
    elif acao == 2:
        print("\nUSUÁRIOS", end="")
        usuarios = visualizarUsuarios()
        selecionarUsuarios(usuarios)
    elif acao == 3:
        print("\nEMAIL USUÁRIOS:")
        listarEmailsUsuarios()
        email = input("\nDigite o email do usuário que deseja visualizar: ")
        usuario = visualizarUsuario(email)
        print("\nUSUÁRIO ESCOLHIDO", end='')
        selecionarUsuario(usuario)
    elif acao == 4:
        print("\nATUALIZAR \nEMAIL USUÁRIOS:")
        listarEmailsUsuarios()
        email = input("\nDigite o email cadastrado do usuário que deseja atualizar: ")
        atualizarUsuario(email)
        print('\nUsuário atualizado com sucesso!')
    elif acao == 5:
        print("\nADICIONAR FAVORITOS \nEMAIL USUÁRIOS:")
        listarEmailsUsuarios()
        email = input("\nDigite o email do usuário em que se deseja adicionar favorito(s): ")
        adicionarFavoritos(email)
        print('Favorito adicionado com sucesso!')
    elif acao == 6:
        print("\nDELETAR \nEMAIL USUÁRIOS:")
        listarEmailsUsuarios()
        email = input("\nDigite o email do usuário que deseja deletar: ")
        deletarUsuario(email)
        print(f'\nUsuário deletado com sucesso!')

    if acao != 0:
        menuUsuario()


def listarEmailsUsuarios():
    result = graph.run("MATCH (u:Usuario) RETURN u.email")  
    found_users = list(result)
    for found in found_users:
        email = found[0].strip("'") 
        print(email)


def selecionarUsuario(lista):
    for usuarioObj in lista:
        for usuario in usuarioObj:
            print(f"\nNome: {usuario['nome']} \nEmail: {usuario['email']} \nCPF: {usuario['cpf']}")
            enderecos = usuario['enderecos']
            for endereco in enderecos:
                endereco = json.loads(endereco)
                cep = endereco['cep']
                num = endereco['num']
                complemento = endereco['complemento']
                print(f"CEP: {cep} Número: {num} Complemento: {complemento}")


def selecionarUsuarios(lista):
    for usuario in lista:
        print(f"\nNome: {usuario['nome']} \nEmail: {usuario['email']} \nCPF: {usuario['cpf']}")
        enderecos = usuario['enderecos']
        for endereco in enderecos:
            endereco = json.loads(endereco)
            cep = endereco['cep']
            num = endereco['num']
            complemento = endereco['complemento']
            print(f"CEP: {cep} Número: {num} Complemento: {complemento}")


def inserirUsuario():
    nome = input('Digite o nome do usuário: ')
    email = input('Digite seu email: ')
    cpf = input("Digite o cpf: ")
    enderecos = []
    repetir = 'S'

    while (repetir != "N"):
        cep = input("Digite o cep: ")
        num = input("Digite o número: ")
        desejo = input("Deseja adicionar um complemento? S/N ")
        if desejo == "S":
            complemento = input("Digite o complemento: ")
        else:
            complemento = ''
        endereco = {"cep": cep, "num": num, "complemento": complemento}
        enderecos.append(json.dumps(endereco)) 
        repetir = input("Digitar outro endereço (S/N)? ")

    node = Node("Usuario", email=email, cpf=cpf, enderecos=enderecos, nome=nome)
    graph.create(node)


def visualizarUsuarios():
    result = graph.run("MATCH (u:Usuario) RETURN u.nome AS nome, u.email AS email, u.cpf AS cpf, u.enderecos AS enderecos, u.nome_favorito AS nome_favorito, u.preco AS preco")
    return result.data()


def visualizarUsuario(email):
    result = graph.run("MATCH (u:Usuario {email: $email}) RETURN u", email=email)  
    found_users = list(result)
    return found_users
        

def atualizarUsuario(email):
    novosValores = {}
    desejo = input("Deseja atualizar o nome? S/N ")
    if desejo == "S":
        novoNome = input("\nDigite o novo nome do usuário: ")
        novosValores["nome"] = novoNome
    desejo = input("Deseja atualizar o email? S/N ")
    if desejo == "S":
        novoEmail = input("Digite o novo email: ")
        novosValores["email"] = novoEmail
    desejo = input("Deseja atualizar o CPF? S/N ")
    if desejo == "S":
        novoCpf = input("Digite o novo CPF: ")
        novosValores["cpf"] = novoCpf
    graph.run("MATCH (u:Usuario {email: $email}) SET u += $novosValores", email=email, novosValores=novosValores)

def adicionarFavoritos(email):
    produtos = []
    print("PRODUTOS")
    listarNomesProdutos()
    nome = input("Digite o nome do produto que deseja favoritar: ")
    result = graph.run("MATCH (u:Produto {nome: $nome}) RETURN ID(u) AS idProduto", nome=nome)
    idProduto = result.evaluate("idProduto")
    produtos.append(idProduto)
    graph.run("MATCH (u:Usuario {email: $email}) UNWIND $produtos AS produto MATCH (p:Produto) WHERE ID(p) = produto CREATE (u)-[:FAVORITOU]->(p)", email=email, produtos=produtos)

def deletarUsuario(email):
    query = ("MATCH (u:Usuario) WHERE u.email = $email DETACH DELETE u")
    graph.run(query, email=email)
