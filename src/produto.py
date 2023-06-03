import pymongo
from pymongo.server_api import ServerApi

client = pymongo.MongoClient("mongodb+srv://juliagayotto:permanganatodepotassio@banco.tltf4oc.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))

db = client.test

global mydb
mydb = client.mercadoLivre

def menuProduto():
    print("\nPRODUTOS")
    print("Escolha uma ação \n")
    print(" 1 - Adicionar produto \n 2 - Visualizar todos produtos \n 3 - Visualizar produto \n 4 - Atualizar produto \n 5 - Deletar produto \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0,1,2,3,4,5]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))

    if acao == 1:
        print("\nCADASTRO")
        inserirProduto()
        print(f'\nProduto cadastrado com sucesso!')
    elif acao == 2:
        print("\nPRODUTOS")
        produtos = visualizarProdutos()
        for produto in produtos:
            print(f"\nNome: {produto.get('nome')} \nPreço: {produto.get('preco')} \nQuantidade: {produto.get('quant_produto')}")
    elif acao == 3:
        print("\nPRODUTOS:")
        listarNomesProdutos()
        nome = input("\nDigite o nome do produto que deseja visualizar: ")
        produto = visualizarProduto(nome)
        print("\nPRODUTO ESCOLHIDO")
        print(f"\nNome: {produto.get('nome')} \nPreço: {produto.get('preco')} \nQuantidade: {produto.get('quant_produto')}")
    elif  acao == 4:
        print("\nATUALIZAR \nPRODUTOS:")
        listarNomesProdutos()
        nome = input("\nDigite o nome do produto que deseja atualizar: ")
        atualizarProduto(nome)
        print(f'\nProduto atualizado com sucesso!')
    elif  acao == 5:
        print("\nDELETAR")
        print("\nPRODUTOS:")
        listarNomesProdutos()
        nome = input("\nDigite o nome do produto que deseja deletar: ")
        deletarProduto(nome) 
        print(f'\nProduto deletado com sucesso!')       

    if acao != 0:
        menuProduto()


def listarNomesProdutos():
    produtos = visualizarProdutos()
    for produto in produtos:
        print(produto.get('nome'))


def inserirProduto():
    global mydb
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preço (XX.XX): R$"))
    quant_produto = int(input("Digite a quantidade do produto: "))
    mydict = {"nome": nome, "preco": preco, "quant_produto": quant_produto}
    mycol = mydb.produto
    return mycol.insert_one(mydict)


def visualizarProdutos():
    global mydb
    mycol = mydb.produto
    return mycol.find()


def visualizarProduto(nome):
    global mydb
    mycol = mydb.produto
    myquery = { "nome": nome }
    return mycol.find_one(myquery)


def atualizarProduto(nome):
    global mydb
    mycol = mydb.produto
    novosValores = {}
    desejo = input("Deseja atualizar o nome? S/N ")
    if desejo == "S":
        novoNome = input("Digite o novo nome do produto: ")
        novosValores["nome"] = novoNome
    desejo = input("Deseja atualizar o preço? S/N ")
    if desejo == "S":
        novoPreco = float(input("Digite o novo preço do produto (XX.XX): R$"))
        novosValores["preco"] = novoPreco
    desejo = input("Deseja atualizar a quantidade em estoque? S/N ")
    if desejo == "S":
        novaQuantidade = int(input("Digite a nova quantidade: "))
        novosValores["quant_produto"] = novaQuantidade
    return mycol.update_one({"nome": nome}, { "$set": novosValores})


def deletarProduto(nome):
    global mydb
    mycol = mydb.produto
    myquery = { "nome": nome }
    return mycol.delete_one(myquery)
