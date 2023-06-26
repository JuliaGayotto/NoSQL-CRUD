import json
from neo4j import GraphDatabase
from produto import visualizarProdutos, visualizarProduto, listarNomesProdutos

driver = GraphDatabase.driver("neo4j+ssc://16df7b0f.databases.neo4j.io", auth=("neo4j", "v4MKtvAydl1gg6a9yuXTcYJGToPJ_rJVVNs0O8fZ6Hw"))

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
        for usuario in usuarios:
            selecionarUsuario(usuario)
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
    with driver.session() as session:
        result = session.run("MATCH (u:Usuario) RETURN u.email")
        for record in result:
            print(record["u.email"])


def selecionarUsuario(usuario):
    print(f"\n\nNome: {usuario['nome']} \nEmail: {usuario['email']} \nCPF: {usuario['cpf']}")
    print(f"CEP: {usuario['cep']} Numero: {usuario['num']} Complemento: {usuario['complemento']}")
    if usuario['nome_favorito']  != None:
        print(f"\nFAVORITO: Nome: {usuario['nome_favorito']}  Preço: R${usuario['preco']}")


def inserirUsuario():
    nome = input("Digite o nome completo do usuário: ")
    email = input("Digite o email: ")
    cpf = input("Digite o CPF: ")
    cep = input("Digite o CEP: ")
    num = input("Digite o número: ")
    desejo = input("Deseja adicionar um complemento? S/N ")
    if desejo == "S":
        complemento = input("Digite o complemento: ")
    else:
        complemento = ''

    with driver.session() as session:
        session.run("CREATE (u:Usuario {nome: $nome, email: $email, cpf: $cpf, cep: $cep, num: $num, complemento: $complemento})",
        nome=nome, email=email, cpf=cpf, cep=cep, num=num, complemento=complemento)


def visualizarUsuarios():
    with driver.session() as session:
        result = session.run("MATCH (u:Usuario) RETURN u.nome AS nome, u.email AS email, u.cpf AS cpf, u.cep AS cep, u.num AS num, u.complemento AS complemento, u.nome_favorito AS nome_favorito, u.preco AS preco")
        return result.data()


def visualizarUsuario(email):
    with driver.session() as session:
        result = session.run("MATCH (u:Usuario {email: $email}) RETURN u", email=email)
        return result.single()[0]
        

def atualizarUsuario(email):
    with driver.session() as session:
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
        session.run("MATCH (u:Usuario {email: $email}) SET u += $novosValores", email=email, novosValores=novosValores)


def adicionarFavoritos(email):
    favoritos = {}
    print("PRODUTOS")
    listarNomesProdutos()
    favorito = input("Digite o nome do produto que deseja favoritar: ")
    produtoFavoritado = visualizarProduto(favorito)
    nome_favorito =  produtoFavoritado["nome"],
    favoritos['nome_favorito'] = nome_favorito
    preco= produtoFavoritado["preco"]
    favoritos['preco'] = preco

    with driver.session() as session:
        session.run("MATCH (u:Usuario {email: $email}) SET  u += $favoritos", email=email, favoritos=favoritos)

def deletarUsuario(email):
    with driver.session() as session:
        session.run(
            "MATCH (u:Usuario {email: $email}) "
            "DELETE u",
            email=email
        )