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
        id = input("Digite o id da compra que deseja visualizar: ")
        visualizarCompra(id)
    elif  acao == 4:
        atualizarCompra()
    elif  acao == 5:
        deletarCompra()

    if acao != 0:
        menuCompra()

    
def inserirCompra():
    global mydb
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preço: "))
    quant_produto = int(input("Digite a quantidade do produto: "))
    produto = {"nome": nome, "preco": preco, "quant_produto": quant_produto}
    nome = input("Digite o nome completo do vendedor: ")
    email = input("Digite o email: ")
    cpf = input("Digite o cpf: ")
    vendedor = {"nome": nome, "email": email, "cpf": cpf}
    preco = float(input("Digite o preço: "))
    quant_produto = int(input("Digite a quantidade do produto: "))
    usuario = inserirUsuario()
    mydict = {"nome": nome, "preco": preco, "quant_produto": quant_produto, "usuario": usuario, "produto": produto, "vendedor": vendedor}
    mycol = mydb.compra
    x = mycol.insert_one(mydict)
    print(x.inserted_id)

def visualizarCompras():
    global mydb
    mycol = mydb.compras
    for x in mycol.find():
        print(x)


def visualizarCompra(id):
    global mydb
    mycol = mydb.compras
    myquery = { "id": ObjectId(id) }
    print(mycol.find_one(myquery))


def atualizarProduto():
    global mydb
    nome = input("Digite o id da compra cadastrada que deseja atualizar: ")
    myquery = visualizarCompra(id)
    mycol = mydb.compra
    novoNome = input("Digite o nome do produto: ")
    novoPreco = float(input("Digite o preço: "))
    novaQuantidade = int(input("Digite a quantidade do produto: "))
    novoProduto = {"nome": novoNome, "preco": novoPreco, "quant_produto": novaQuantidade}
    novoNome = input("Digite o nome completo do vendedor: ")
    novoEmail = input("Digite o email: ")
    novoCpf = input("Digite o cpf: ")
    novoVendedor = {"nome": novoNome, "email": novoEmail, "cpf": novoCpf}
    novoPreco = float(input("Digite o preço: "))
    novaQuant_produto = int(input("Digite a quantidade do produto: "))
    novoUsuario = inserirUsuario()
    # , "usuario": usuario, "produto": produto, "vendedor": vendedor}
    newvalues = { "$set": { "nome": novoNome}, "$set": { "preco": novoPreco },
                  "$set": { "quant_produto": novaQuantidade }}
    print(mycol.update_one(myquery, newvalues))

def deletarCompra(id):
    global mydb
    mycol = mydb.compras
    mydict = { "id": ObjectId(id) }
    result = mycol.delete_one(mydict)
    print(result)