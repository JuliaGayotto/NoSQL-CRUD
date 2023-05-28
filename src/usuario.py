from produto import visualizarProdutos, visualizarProduto, listarNomesProdutos
from bson import ObjectId
import pymongo
from pymongo.server_api import ServerApi

client = pymongo.MongoClient("mongodb+srv://juliagayotto:permanganatodepotassio@banco.tltf4oc.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.test

global mydb
mydb = client.mercadoLivre

def menuUsuario():
    print("\n\nUSUÁRIOS")
    print("Escolha uma ação: \n")
    print(" 1 - Adicionar usuário \n 2 - Visualizar todos usuários \n 3 - Visualizar usuário \n 4 - Atualizar usuário \n 5 - Adicionar favoritos \n 6 - Deletar usuário \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0,1,2,3,4,5,6]
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
        email = input("\nDigite o email do usuario que deseja visualizar: ")
        usuario = visualizarUsuario(email)
        print("\nUSUÁRIO ESCOLHIDO", end='')
        selecionarUsuario(usuario)   
    elif  acao == 4:
        print("\nATUALIZAR \nEMAIL USUÁRIOS:")
        listarEmailsUsuarios()
        email = input("\nDigite o email cadastrado do usuario que deseja atualizar: ")
        atualizarUsuario(email)
        print('\nUsuário atualizado com sucesso!')
    elif  acao == 5:
        print("\nADICIONAR FAVORITOS \nEMAIL USUÁRIOS:")
        listarEmailsUsuarios()
        email = input("\nDigite o email do usuário em que se deseja adicionar favorito(s): ")
        adicionarFavoritos(email)
        print('\nFavorito adicionado com sucesso!')
    elif  acao == 6:
        print("\nDELETAR \nEMAIL USUÁRIOS:")
        listarEmailsUsuarios()
        email = input("\nDigite o email do usuário que deseja deletar: ")
        deletarUsuario(email)
        print(f'\nUsuário deletado com sucesso!')
        
    if acao != 0:
        menuUsuario()


def listarEmailsUsuarios():
    usuarios = visualizarUsuarios()
    for usuario in usuarios:
        print(usuario.get('email'))
        

def selecionarUsuario(usuario):
    print(f"\n\nNome: {usuario.get('nome')} \nEmail: {usuario.get('email')} \nCPF: {usuario.get('cpf')}", end='')       
    enderecos = usuario.get("enderecos")
    for endereco in enderecos:
        cep = endereco.get("cep")
        numero = endereco.get("numero")
        complemento = endereco.get("complemento")
        print(f"\nENDEREÇO: \nCEP: {cep}  Número: {numero} ", end='')
        if complemento != '':
            print(f"Complemento: {complemento}", end='')
    favoritos = usuario.get("favoritos")
    if favoritos != None:
        for favorito in favoritos:
            nome = favorito.get("nome_favorito")
            preco = favorito.get("preco")
            print(f"\nFAVORITO: Nome: {nome}  Preço: R${preco}", end='')


def inserirUsuario():
    global mydb
    nome = input("Digite o nome completo do usuário: ")
    email = input("Digite o email: ")
    cpf = input("Digite o CPF: ")
    enderecos = []
    repetir = 'S'

    while (repetir != "N"):
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

    mydict = {"nome": nome, "email": email, "cpf": cpf, "enderecos" : enderecos}
    mycol = mydb.usuario
    return mycol.insert_one(mydict)


def visualizarUsuarios():
    global mydb
    mycol = mydb.usuario
    return mycol.find()


def visualizarUsuario(email):
    global mydb
    mycol = mydb.usuario
    myquery = { "email": email }
    return mycol.find_one(myquery)


def atualizarUsuario(email):
    global mydb
    mycol = mydb.usuario
    novoNome = input("Digite o novo nome do usuario: ")
    novoEmail = input("Digite o novo email: ")
    novoCpf = input("Digite o novo CPF: ")
    novosEnderecos = []
    repetir = 'S'
    
    while (repetir != "N"):
        cep = input("Digite o CEP: ")
        num = int(input("Digite o número: "))
        desejo = input("Deseja alterar o complemento? S/N ")
        if desejo == "S":
            complemento = input("Digite o complemento: ")
        else:
            complemento = ''
        end = {"cep": cep, "numero": num, "complemento": complemento}
        novosEnderecos.append(end)
        repetir = input("Digitar outro endereço (S/N)? ")

    novosValores = {"nome": novoNome, "email": novoEmail, "cpf": novoCpf, "enderecos" : novosEnderecos}
    return mycol.update_one({"email": email}, { "$set": novosValores})


def adicionarFavoritos(email):
    favoritos = []
    desejo = "S"
    while (desejo != "N"):
        print("PRODUTOS")
        listarNomesProdutos()
        favorito = input("Digite o nome do produto que deseja favoritar: ")
        produtoFavoritado = visualizarProduto(favorito)  
        print(produtoFavoritado)
        favorito = {"_id": ObjectId(), "nome_favorito": produtoFavoritado["nome"],"preco": produtoFavoritado["preco"]}
        favoritos.append(favorito)
        desejo = input("Deseja adicionar outro produto em favoritos? S/N ")
    novoValor = {"favoritos": favoritos}
    mycol = mydb.usuario
    return mycol.update_one({"email": email}, { "$set": novoValor})


def deletarUsuario(email):
    global mydb
    mycol = mydb.usuario
    myquery = { "email": email }
    return mycol.delete_one(myquery)
