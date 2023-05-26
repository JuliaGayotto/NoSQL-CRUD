from produto import visualizarProdutos, visualizarProduto
import pymongo
from pymongo.server_api import ServerApi

client = pymongo.MongoClient("mongodb+srv://juliagayotto:permanganatodepotassio@banco.tltf4oc.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))

db = client.test

global mydb
mydb = client.mercadoLivre

def menuUsuario():
    print("\nUsuários")
    print("Escolha uma ação: \n")
    print(" 1 - Adicionar usuário \n 2 - Visualizar todos usuários \n 3 - Visualizar usuário \n 4 - Atualizar usuário \n 5 - Adicionar favoritos \n 6 - Deletar usuário \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0,1,2,3,4,5,6]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))

    if acao == 1:
       inserirUsuario()
       print(f'\nUsuario cadastrado com sucesso!')
    elif acao == 2:
        visualizarUsuarios()
    elif acao == 3:
        email = input("Digite o email do usuario que deseja visualizar: ")
        visualizarUsuario(email)
    elif  acao == 4:
        visualizarUsuarios()
        email = input("\nDigite o email cadastrado do usuario que deseja atualizar: ")
        atualizarUsuario(email)
        print(f'\nUsuário atualizado com sucesso!')
    elif  acao == 5:
        visualizarUsuarios()
        email = input("\nDigite o email do usuário em que se deseja adicionar favorito(s): ")
        adicionarFavoritos(email)
        print(f'\nFavorito adicionado com sucesso!')
    elif  acao == 6:
        deletarUsuario()
        print(f'\nUsuário deletado com sucesso!')
        
    if acao != 0:
        menuUsuario()


def inserirUsuario():
    global mydb
    nome = input("Digite o nome completo do usuário: ")
    email = input("Digite o email: ")
    cpf = input("Digite o CPF: ")
    endereco = []
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
        endereco.append(end)
        repetir = input("Digitar outro endereço (S/N)? ")

    mydict = {"nome": nome, "email": email, "cpf": cpf, "endereco" : endereco}
    mycol = mydb.usuario
    mycol.insert_one(mydict)


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


def atualizarUsuario(email):
    global mydb
    mycol = mydb.usuario
    novoNome = input("Digite o novo nome do usuario: ")
    novoEmail = input("Digite o novo email: ")
    novoCpf = input("Digite o novo CPF: ")
    novoEndereco= []
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
        novoEndereco.append(end)
        repetir = input("Digitar outro endereço (S/N)? ")

    novosValores = {"nome": novoNome, "email": novoEmail, "cpf": novoCpf, "endereco" : novoEndereco}
    mycol.update_one({"email": email}, { "$set": novosValores})


def adicionarFavoritos(email):
    visualizarProdutos()
    favoritos = []
    desejo = "S"
    while (desejo != "N"):
        favorito = input("\n Digite o nome do produto que deseja favoritar: ")
        produtoFavoritado = visualizarProduto(favorito)  
        favorito = {"nome_favorito": produtoFavoritado["nome"],"preco": produtoFavoritado["preco"]}
        favoritos.append(favorito)
        desejo = input("Deseja adicionar outro produto em favoritos? S/N ")
    novoValor = {"favoritos": favoritos}
    mycol = mydb.usuario
    mycol.update_one({"email": email}, { "$set": novoValor})


def deletarUsuario(nome):
    global mydb
    mycol = mydb.usuario
    myquery = { "nome": nome }
    print(mycol.delete_one(myquery))
    print(f'Usuario deletdo com sucesso!')
