from bson import ObjectId
import pymongo
from pymongo.server_api import ServerApi

client = pymongo.MongoClient("mongodb+srv://juliagayotto:permanganatodepotassio@banco.tltf4oc.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))

db = client.test

global mydb
mydb = client.mercadoLivre

def menuCompra():
    print("\n Compra")
    print("Escolha uma ação \n")
    print(" 1 - Adicionar compras \n 2 - Visualizar todas as compras \n 3 - Visualizar compra \n 4 - Atualizar compra \n 5 - Deletar compra \n  0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0,1,2,3,4,5]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))

    if acao == 1:
       inserirCompra()
    elif acao == 2:
        visualizarCompras()
    elif acao == 3:
        visualizarCompra()
    elif  acao == 4:
        atualizarCompra()
    elif  acao == 5:
        deletarCompra()
       

    if acao != 0:
        menuCompra()

def visualizarCompras():
    global mydb
    mycol = mydb.produto
    for x in mycol.find():
        print(x)


def visualizarCompra(id):
    global mydb
    mycol = mydb.produto
    myquery = { "id": ObjectId(id) }
    print(mycol.find_one(myquery))


def deletarCompra(id):
    global mydb
    mycol = mydb.compras
    mydict = { "id": ObjectId(id) }
    result = mycol.delete_one(mydict)
    print(result)