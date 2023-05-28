from bson import ObjectId
from usuario import visualizarUsuario, listarEmailsUsuarios
from produto import visualizarProduto, listarNomesProdutos
from vendedor import visualizarVendedor, listarEmailsVendedores
import pymongo
from pymongo.server_api import ServerApi

client = pymongo.MongoClient("mongodb+srv://juliagayotto:permanganatodepotassio@banco.tltf4oc.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.test

global mydb
mydb = client.mercadoLivre

def menuCompra():
    print("\nCOMPRAS")
    print("Escolha uma ação \n")
    print(" 1 - Adicionar compra \n 2 - Visualizar todas as compras \n 3 - Visualizar compra \n 4 - Deletar compra \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0,1,2,3,4]
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
            selecionarCompra(compra)    
    elif acao == 3:
        id = input("Digite o id da compra que deseja visualizar: ")
        compra = visualizarCompra(id)
        print("\nCOMPRA ESCOLHIDA")
        selecionarCompra(compra) 
    elif  acao == 4:
        print("\nDELETAR")
        id = input("Digite o id da compra que deseja deletar: ")
        deletarCompra(id)
        print(f'\nCompra deletada com sucesso!')
        
    if acao != 0:
        menuCompra()


def selecionarCompra(compra):
    print(f"\nId da compra: {compra.get('_id')}")
    print(f"Data da Compra: {compra.get('data_compra')}")
    usuario = compra.get("usuario")
    print(f"Usuário:  Nome: {usuario.get('nome')}  Email: {usuario.get('email')}  CPF: {usuario.get('cpf')}")
    vendedor = compra.get("vendedor")
    print(f"Vendedor:  Nome: {vendedor.get('nome_vendedor')}  Email: {vendedor.get('email')}  CPF: {vendedor.get('cpf')}")
    produtos = compra.get('produtos')
    for produto in produtos:
        print(f"Produto:  Nome: {produto.get('nome')}  Preço: {produto.get('preco')}  Quantidade comprada: {produto.get('quant_comprada')}")
    

def inserirCompra():
    global mydb
    dataCompra = input("Digite a data da compra: ")
    produtos = []
    desejo  = 'S'
    print("PRODUTOS")
    listarNomesProdutos()

    while desejo != "N":
        nomeProduto = input("Digite o nome do produto: ")
        quant = int(input("Digite a quantidade comprada: "))
        prod = visualizarProduto(nomeProduto)
        produto = {"id": prod.get('_id'), "nome": prod.get('nome'), "preco": prod.get('preco'), "quant_comprada": quant }
        produtos.append(produto)
        desejo = input("Deseja adicionar outro produto à compra? S/N ")

    print("EMAILS VENDEDORES:")
    listarEmailsVendedores()
    emailVendedor = input("Digite o email do vendedor: ")
    vend = visualizarVendedor(emailVendedor)
    vendedor = {"id": vend.get('_id'), "nome_vendedor": vend.get('nome_vendedor'), "email": vend.get('email'), "cpf": vend.get('cpf')}
    print("EMAIL USUÁRIOS:")
    listarEmailsUsuarios()  
    emailUsuario = input("Digite o email do usuario: ")
    usu = visualizarUsuario(emailUsuario)
    usuario = {"id": usu.get('_id'), "nome": usu.get('nome'), "email": usu.get('email'), "cpf": usu.get('cpf')}

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


def deletarCompra(id):
    global mydb
    mycol = mydb.compra
    mydict = { "_id": ObjectId(id) }
    return mycol.delete_one(mydict)
    