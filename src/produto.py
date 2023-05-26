import pymongo
from pymongo.server_api import ServerApi

client = pymongo.MongoClient("mongodb+srv://juliagayotto:permanganatodepotassio@banco.tltf4oc.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))

db = client.test

global mydb
mydb = client.mercadoLivre

def menuProduto():
    print("\n Produto")
    print("Escolha uma ação \n")
    print(" 1 - Adicionar produto \n 2 - Visualizar todos produtos \n 3 - Visualizar produto \n 4 - Atualizar produto \n 5 - Deletar produto \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0,1,2,3,4,5]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))

    if acao == 1:
        inserirProduto()
        print(f'\nProduto cadastrado com sucesso!')
    elif acao == 2:
        visualizarProdutos()
    elif acao == 3:
        nome = input("Digite o nome do produto que deseja visualizar: ")
        visualizarProduto(nome)
    elif  acao == 4:
        visualizarProdutos()
        nome = input("Digite o nome do produto que deseja atualizar: ")
        atualizarProduto(nome)
        print(f'\nProduto atualizado com sucesso!')
    elif  acao == 5:
        nome = input("Digite o nome do produto que deseja deletar: ")
        deletarProduto(nome) 
        print(f'\nProduto deletdo com sucesso!')       

    if acao != 0:
        menuProduto()


def inserirProduto():
    global mydb
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preço: "))
    quant_produto = int(input("Digite a quantidade do produto: "))
    mydict = {"nome": nome, "preco": preco, "quant_produto": quant_produto}
    mycol = mydb.produto
    x = mycol.insert_one(mydict)
    print(x.inserted_id)


def visualizarProdutos():
    global mydb
    mycol = mydb.produto
    for x in mycol.find():
        print(x)


def visualizarProduto(nome):
    global mydb
    mycol = mydb.produto
    myquery = { "nome": nome }
    print(mycol.find_one(myquery))
    return mycol.find_one(myquery)


def atualizarProduto(nome):
    global mydb
    mycol = mydb.produto
    novoNome = input("Digite o novo nome do produto: ")
    novoPreco = float(input("Digite o novo preço do produto (XX.XX): R$"))
    novaQuantidade = int(input("Digite a nova quantidade: "))
    novosValores = { "nome": novoNome, "preco": novoPreco, "quant_produto": novaQuantidade }
    print(mycol.update_one({"nome": nome}, { "$set": novosValores}))


def deletarProduto(nome):
    global mydb
    mycol = mydb.produto
    myquery = { "nome": nome }
    print(mycol.delete_one(myquery))
