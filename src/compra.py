from bson import ObjectId
from usuario import visualizarUsuario
from produto import visualizarProduto
from vendedor import visualizarVendedor
import pymongo
from pymongo.server_api import ServerApi

client = pymongo.MongoClient("mongodb+srv://juliagayotto:permanganatodepotassio@banco.tltf4oc.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.test

global mydb
mydb = client.mercadoLivre

def menuCompra():
    print("\nCOMPRA")
    print("Escolha uma ação \n")
    print(" 1 - Adicionar compras \n 2 - Visualizar todas as compras \n 3 - Visualizar compra \n 4 - Atualizar compra \n 5 - Deletar compra \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0,1,2,3,4,5]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))

    if acao == 1:
        print("\nCADASTRO")
        inserirCompra()
        print(f'\nCompra cadastrada com sucesso!')
    elif acao == 2:
        print("\nCOMPRAS")
        compras = visualizarCompras()
        for compra in compras:
            print(f"\nData da Compra: {compra.get('data_compra')} \nUsuario: {compra.get('usuario')} \nVendedor: {compra.get('vendedor')} \nProduto: {compra.get('produtos')}") 
    
    elif acao == 3:
        id = input("Digite o id da compra que deseja visualizar: ")
        compra = visualizarCompra(id)
        print(type(compra))
        print("\nCOMPRA ESCOLHIDA")
        print(f"\nData da Compra: {compra.get('data_compra')} \nUsuario: {compra.get('usuario')} \nVendedor: {compra.get('vendedor')} \nProduto: {compra.get('produtos')}") 
    elif  acao == 4:
        print("\nATUALIZAR \nCOMPRAS:")
        id = input("Digite o id da compra que deseja atualizar: ")
        atualizarCompra(id)
        print(f'\nCompra atualizado com sucesso!')
    
    elif  acao == 5:
        print("\nDELETAR")
        id = input("Digite o id da compra que deseja deletar: ")
        deletarCompra(id)
        print(f'\nProduto deletado com sucesso!')
        
    if acao != 0:
        menuCompra()


def listarCompras():
    print(f"\nId: {produto.get('nome')} \nPreço: {produto.get('preco')} \nQuantidade: {produto.get('quant_produto')}")
    
def inserirCompra():
    global mydb
    dataCompra = input("Digite a data da compra: ")
    produtos = []
    while desejo != "N":
        nomeProduto = input("Digite o nome do produto: ")
        quant = int(input("Digite a quantidade comprada: "))
        prod = visualizarProduto(nomeProduto)
        produto = {"nome": prod.get('nome'), "preco": prod.get('preco'), "quant_comprada": quant }
        produtos.append(produto)
        desejo = input("Deseja adicionar outro produto à compra? S/N")
    emailVendedor = input("Digite o email do vendedor: ")
    vend = visualizarVendedor(emailVendedor)
    vendedor = {"nome_vendedor": vend.get('nome_vendedor'), "email": vend.get('email'), "cpf": vend.get('cpf')}
    emailUsuario = input("Digite o email do usuario: ")
    usu = visualizarUsuario(emailUsuario)
    usuario = {"nome": usu.get('nome'), "email": usu.get('email'), "cpf": usu.get('cpf')}
    mydict = {"data_compra": dataCompra, "usuario": usuario, "produtos": produtos, "vendedor": vendedor}
    mycol = mydb.compra
    return mycol.insert_one(mydict)
    

def visualizarCompras():
    global mydb
    mycol = mydb.compra
    return mycol.find()


def visualizarCompra(id):
    global mydb
    mycol = mydb.compra
    myquery = { "_id": ObjectId(id) }
    return mycol.find_one(myquery)


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
    mycol = mydb.compra
    mydict = { "id": ObjectId(id) }
    print( mycol.delete_one(mydict))