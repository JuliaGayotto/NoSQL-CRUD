import pymongo
import redis
import json
from bson.json_util import dumps
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb+srv://juliagayotto:permanganatodepotassio@banco.tltf4oc.mongodb.net/?retryWrites=true&w=majority")
db = client.test

global mydb
mydb = client.mercadoLivre

dbRedis = redis.Redis(
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
            menuProduto()
            menu()
        case 3:
            menuVendedor()
            menu()
        case 0:
            print("Até mais!")
        case _:
            print("Acão não entendida")
            menu()


def atualizarEmailUsuario(): 
    listarNomesUsuarios()
    nome = input("\nDigite o nome do usuario que deseja alterar o email: ")
    mycol = mydb.usuario
    myquery = {"nome": nome}
    usuario = mycol.find_one(myquery)
    print(usuario)

    emailAntigo = visualizarUsuario(usuario.get('email')).get('email')
    email = input(f"\nDigite o novo email de {nome}: ")
    dbRedis.hset('usuario:' + nome, 'email', email)
    print(dbRedis.hget("usuario:" + nome, 'email'))
    
    mycol.update_one({"nome": nome}, {"$set": {
        "email": json.loads(dbRedis.hget("usuario:" + nome, 'email')),
    }}, upsert=True)
    usuario2 = visualizarUsuario(usuario.get('email'))
    emailUsuario = usuario.get('email')
    print(f'Email de {nome} atualizado com sucesso!')
    print(f'Email antigo: {emailAntigo} \nEmail novo: {emailUsuario}')

def listarNomesUsuarios():
    usuarios = visualizarUsuarios()
    for usuario in usuarios:
        print(usuario.get('nome'))


def visualizarUsuario(email):
    global mydb
    mycol = mydb.usuario
    myquery = { "email": email }
    return mycol.find_one(myquery)


def visualizarUsuarios():
    global mydb
    mycol = mydb.usuario
    return mycol.find()

menu()