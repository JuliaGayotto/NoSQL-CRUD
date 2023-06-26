import pymongo
import redis
import json
from bson import ObjectId, Decimal128

client = pymongo.MongoClient("mongodb+srv://juliagayotto:permanganatodepotassio@banco.tltf4oc.mongodb.net/?retryWrites=true&w=majority")
db = client.test

global mydb
mydb = client.mercadoLivre

client_redis = redis.Redis(
        host='redis-17682.c280.us-central1-2.gce.cloud.redislabs.com',
        port=17682,
        password='Permanganatodepotassio123@')

def menu():
    print('''\nAÇÕES: 
             \n 1 - Atualizar email de um usuário
             \n 2 - Atualizar preço do produto
             \n 3 - Atualizar o nome do vendedor
             \n 0 - Sair ''')
    colecao = int(input("Escolha uma ação: "))
    
    match colecao:
        case 1: 
            atualizarEmailUsuario()
            menu()
        case 2: 
            atualizarPrecoProduto()
            menu()
        case 3:
            atualizarNomeVendedor()
            menu()
        case 0:
            print("Até mais!")
        case _:
            print("Acão não entendida")
            menu()


def atualizarEmailUsuario(): 
    print("USUÁRIOS")
    listarNomesUsuarios()
    nome = input("\nDigite o nome do usuario que deseja alterar o email: ")
    mycol = mydb.usuario
    myquery = {"nome": nome}
    usuario = mycol.find_one(myquery)

    print("Dados atuais no mongo...")
    selecionarUsuario(usuario)
    emailAntigo = usuario.get('email')

    print("\nEnviando os dados atuais para o redis...")
    client_redis.set('usuario:' + nome, emailAntigo)
    print("Dados enviados para o redis com sucesso!")

    email = input(f"\nDigite o novo email de {nome}: ")
    print("\nAtualizando novo email no redis...")
    client_redis.set('usuario:' + nome, email)
    print("Novo email atualizado no redis com sucesso!")
    novo_email = client_redis.get('usuario:' + nome)
    print(f'Email antigo: {emailAntigo} \nEmail novo: {novo_email.decode()}')

    print("\nAtualizando alteração no mongo...")
    mycol.update_one(myquery, {"$set": {
        "email": novo_email.decode()
    }}, upsert=True)
    print("Alteração atualizada no mongo!")

    usuario2 = visualizarUsuario(email)
    emailUsuario = usuario2.get('email')
    print(f'Email de {nome} atualizado com sucesso!')
    print(f'Email antigo: {emailAntigo} \nEmail novo: {emailUsuario}')


def atualizarPrecoProduto():
    print("PRODUTOS:")
    listarNomesProdutos()
    nome = input("\nDigite o nome do produto que deseja alterar o preço: ")
    mycol = mydb.produto
    myquery = {"nome": nome}
    produto = mycol.find_one(myquery)
    
    print("Dados atuais no mongo...")
    selecionarProduto(produto)
    precoAntigo = produto.get('preco')

    print("\nEnviando os dados atuais para o redis...")
    client_redis.set('produto:' + nome, precoAntigo)
    print("Dados enviados para o redis com sucesso!")

    preco = input(f"\nDigite o novo preço de {nome}: ")
    print("\nAtualizando novo preco no redis...")
    client_redis.set('produto:' + nome, preco)
    print("Novo preco atualizado no redis com sucesso!")
    novo_preco = client_redis.get('produto:' + nome)
    print(f'Preco antigo: {precoAntigo} \nPreco novo: {novo_preco.decode()}')

    print("\nAtualizando alteração no mongo...")
    mycol.update_one(myquery, {"$set": {
        "preco": novo_preco.decode()
    }}, upsert=True)
    print("Alteração atualizada no mongo!")

    produto2 = visualizarProduto(nome)
    precoProduto = produto2.get('preco')
    print(f'Preco de {nome} atualizado com sucesso!')
    print(f'Preco antigo: {precoAntigo} \nPreco novo: {precoProduto}')


def atualizarNomeVendedor(): 
    print("VENDEDORES")
    listarEmailsVendedores()
    email = input("\nDigite o email do vendedor que deseja atualizar o nome: ")
    mycol = mydb.vendedor
    myquery = {"email": email}
    vendedor = mycol.find_one(myquery)

    print("Dados atuais no mongo...")
    selecionarVendedor(vendedor)
    nomeAntigo = vendedor.get('nome_vendedor')

    print("\nEnviando os dados atuais para o redis...")
    client_redis.set('vendedor:' + email, nomeAntigo)
    print("Dados enviados para o redis com sucesso!")

    nome = input(f"\nDigite o nome atualizado de {email}: ")
    print("\nAtualizando novo nome no redis...")
    client_redis.set('vendedor:' + email, nome)
    print("Nome atualizado no redis com sucesso!")
    nomeAtualizado = client_redis.get('vendedor:' + email)
    print(f'Nome antigo: {nomeAntigo} \nNome atualizado: {nomeAtualizado.decode()}')

    print("\nAtualizando alteração no mongo...")
    mycol.update_one(myquery, {"$set": {
        "nome_vendedor": nomeAtualizado.decode()
    }}, upsert=True)
    print("Alteração atualizada no mongo!")

    vendedor2 = visualizarVendedor(email)
    nomeVendedor = vendedor2.get('nome_vendedor')
    print(f'Nome de {email} atualizado com sucesso!')
    print(f'Nome antigo: {nomeAntigo} \nNome atualizado: {nomeVendedor}')

#-----------------------------------------------------------------------------------------------------------------

def listarNomesUsuarios():
    usuarios = visualizarUsuarios()
    for usuario in usuarios:
        print(usuario.get('nome'))

def selecionarUsuario(usuario):
    print(f"\nNome: {usuario.get('nome')} \nEmail: {usuario.get('email')}")       

def visualizarUsuario(email):
    global mydb
    mycol = mydb.usuario
    myquery = { "email": email }
    return mycol.find_one(myquery)

def visualizarUsuarios():
    global mydb
    mycol = mydb.usuario
    return mycol.find()

#---------------------------------------------------------------------------------------------------------------------

def listarNomesProdutos():
    produtos = visualizarProdutos()
    for produto in produtos:
        print(produto.get('nome'))

def visualizarProdutos():
    global mydb
    mycol = mydb.produto
    return mycol.find()

def visualizarProduto(nome):
    global mydb
    mycol = mydb.produto
    myquery = { "nome": nome }
    return mycol.find_one(myquery)

def selecionarProduto(produto):
    print(f"\nNome: {produto.get('nome')} \nPreço: {produto.get('preco')}")      

#------------------------------------------------------------------------------------------------------------------------------

def listarEmailsVendedores():
    vendedores = visualizarVendedores()
    for vendedor in vendedores:
        print(vendedor.get('email'))


def visualizarVendedores():
    global mydb
    mycol = mydb.vendedor
    return mycol.find()

def visualizarVendedor(email):
    global mydb
    mycol = mydb.vendedor
    myquery = { "email": email }
    return mycol.find_one(myquery)

def selecionarVendedor(vendedor):
    print(f"\nNome: {vendedor.get('nome_vendedor')} \nEmail: {vendedor.get('email')}")  


menu()