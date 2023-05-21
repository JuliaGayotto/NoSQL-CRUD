from produto import visualizarProdutos
import pymongo
from pymongo.server_api import ServerApi

client = pymongo.MongoClient("mongodb+srv://juliagayotto:permanganatodepotassio@banco.tltf4oc.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))

db = client.test

global mydb
mydb = client.mercadoLivre

def menuUsuario():
    print("\n Usuários")
    print("Escolha uma ação \n")
    print(" 1 - Adicionar usuário \n 2 - Visualizar todos usuários \n 3 - Visualizar usuário \n 4 - Atualizar usuário \n 5 - Adicionar favoritos \n 6 - Deletar usuário \n  0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0,1,2,3,4,5,6]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))

    if acao == 1:
       inserirUsuario()
    elif acao == 2:
        visualizarUsuarios()
    elif acao == 3:
        email = input("Digite o email do usuario que deseja visualizar: ")
        visualizarUsuario(email)
    elif  acao == 4:
        atualizarUsuario()
    elif  acao == 5:
        adicionarFavorito()
    elif  acao == 6:
        deletarUsuario()

    if acao != 0:
        menuUsuario()

def endereco():
    cep = input("Digite o CEP: ")
    num = int(input("Digite o número: "))
    desejo = input("Deseja adicionar um complemento? S/N ")
    if desejo == "S":
        complemento = input("Digite o complemento: ")
    else:
        complemento = ''
    end = {"cep": cep, "numero": num, "complemento": complemento}
    return end 

def favorito():
    favoritos = []
    visualizarProdutos()
    favorito = input("\n Digite o nome do produto que deseja favoritar: ")
    desejo = input("Deseja adicionar outro produto em favoritos? S/N ")
    while (desejo != "N"):
        favorito = input("\n Digite o nome do produto que deseja favoritar: ")
        favoritos.append(favorito)
    return favoritos


def inserirUsuario():
    global mydb
    nome = input("Digite o nome completo do usuário: ")
    email = input("Digite o email: ")
    cpf = input("Digite o CPF: ")
    endereco = []
    repetir = 'S'

    while (repetir != "N"):
        endereco.append(endereco())
        repetir = input("Digitar outro endereço (S/N)? ")

    desejo = input("Deseja adicionar algum produto em favoritos? S/N ")
    if desejo == "S":
        favoritos = favorito()
       
    mydict = {"nome": nome, "email": email, "cpf": cpf, "endereco" : endereco, "favoritos": favoritos}
    mycol = mydb.usuario
    x = mycol.insert_one(mydict)
    print(x.inserted_id)
    print(f'Usuario cadastrado com sucesso!')
 

def visualizarUsuarios():
    global mydb
    mycol = mydb.usuario
    for x in mycol.find():
        print(x)


def visualizarUsuario(email):
    global mydb
    mycol = mydb.usuario
    myquery = { "email": email }
    print(mycol.find_one(myquery))


def atualizarUsuario():
    email = input("Digite o email cadastrado do usuario que deseja atualizar: ")
    myquery = visualizarUsuario(email)
    mycol = mydb.usuario
    novoNome = input("Digite o novo nome do usuario")
    novoEmail = input("Digite o novo email: ")
    novoCpf = input("Digite o novo CPF: ")
    novoEndereco= []
    repetir = 'S'
    
    while (repetir != "N"):
        endereco.append(endereco())
        repetir = input("Atualizar outro endereço (S/N)? ")

    favoritos = favorito()
    newvalues = { "$set": { "nome": novoNome}, "$set": { "email": novoEmail },
                  "$set": { "Cpf": novoCpf }, "$set": { "endereco" : novoEndereco }, "$set": { "favoritos": favoritos} }
    mydict = {"nome": novoNome, "email": novoEmail, "cpf": novoCpf, "endereco" : novoEndereco, "favoritos": favoritos}
    mycol = mydb.usuario
    print(mycol.update_one(myquery, newvalues))
    print(f'\n Usuário atualizado com sucesso!')


def adicionarFavoritos():
    return ["fav"]


def deletarUsuario(nome):
    global mydb
    mycol = mydb.usuario
    myquery = { "nome": nome }
    print(mycol.delete_one(myquery))
    print(f'Usuario deletdo com sucesso!')
