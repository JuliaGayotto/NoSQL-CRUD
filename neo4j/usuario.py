from neo4j import GraphDatabase
from produto import visualizarProdutos, visualizarProduto, listarNomesProdutos

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

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
    print(f"\n\nNome: {usuario['nome']} \nEmail: {usuario['email']} \nCPF: {usuario['cpf']}", end='')
    enderecos = usuario.get("enderecos", [])
    for endereco in enderecos:
        cep = endereco["cep"]
        numero = endereco["numero"]
        complemento = endereco["complemento"]
        print(f"\nENDEREÇO: \nCEP: {cep}  Número: {numero} ", end='')
        if complemento:
            print(f"Complemento: {complemento}", end='')
    favoritos = usuario.get("favoritos")
    if favoritos:
        for favorito in favoritos:
            nome = favorito["nome_favorito"]
            preco = favorito["preco"]
            print(f"\nFAVORITO: Nome: {nome}  Preço: R${preco}", end='')

def inserirUsuario():
    nome = input("Digite o nome completo do usuário: ")
    email = input("Digite o email: ")
    cpf = input("Digite o CPF: ")
    enderecos = []
    repetir = 'S'

    while repetir != "N":
        cep = input("Digite o CEP: ")
        num = int(input("Digite o número: "))
        desejo = input("Deseja adicionar um complemento? S/N ")
        if desejo == "S":
            complemento = input("Digite o complemento: ")
        else:
            complemento = ''
        end = {"cep": cep, "numero": num, "complemento": complemento}
        enderecos.append(end)
        repetir = input("Digitar outro endereço (S/N)? ")

    with driver.session() as session:
        session.run(
            """
            CREATE (usuario:Usuario {nome: $nome, email: $email, cpf: $cpf, enderecos: $enderecos})
            """,
            nome=nome,
            email=email,
            cpf=cpf,
            enderecos=enderecos
        )

def visualizarUsuarios():
    with driver.session() as session:
        result = session.run("MATCH (usuario:Usuario) RETURN usuario")
        return result.records()

def visualizarUsuario(email):
    with driver.session() as session:
        result = session.run("MATCH (usuario:Usuario {email: $email}) RETURN usuario", email=email)
        record = result.single()
        if record:
            return record["usuario"]
        else:
            return None

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

    with driver.session() as session:
        result = session.run(
            "MATCH (u:Usuario {email: $email}) "
            "SET u += $novosValores "
            "RETURN u",
            email=email,
            novosValores=novosValores
        )
        return result.single()

def adicionarFavoritos(email):
    favoritos = []
    desejo = "S"
    while desejo != "N":
        print("PRODUTOS")
        listarNomesProdutos()
        favorito = input("Digite o nome do produto que deseja favoritar: ")
        produtoFavoritado = visualizarProduto(favorito)
        favorito = {
            "_id": str(uuid.uuid4()),
            "nome_favorito": produtoFavoritado["nome"],
            "preco": produtoFavoritado["preco"]
        }
        favoritos.append(favorito)
        desejo = input("Deseja adicionar outro produto em favoritos? S/N ")

    with driver.session() as session:
        session.run(
            "MATCH (u:Usuario {email: $email}) "
            "SET u.favoritos = $favoritos",
            email=email,
            favoritos=favoritos
        )

def deletarUsuario(email):
    with driver.session() as session:
        session.run(
            "MATCH (u:Usuario {email: $email}) "
            "DELETE u",
            email=email
        )