import pymongo
from pymongo.server_api import ServerApi

client = pymongo.MongoClient("mongodb+srv://juliagayotto:permanganatodepotassio@banco.tltf4oc.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))

db = client.test

global mydb
mydb = client.mercadoLivre

def menuVendedor():
    print("\n VENDEDORES")
    print("Escolha uma ação \n")
    print(" 1 - Adicionar vendedor \n 2 - Visualizar todos vendedores \n 3 - Visualizar vendedor \n 4 - Atualizar vendedor \n 5 - Deletar vendedor \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0,1,2,3,4,5]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))

    if acao == 1:
        print("\nCADASTRO")
        inserirVendedor()
        print(f'\nVendedor cadastrado com sucesso!')
    elif acao == 2:
        print("\nVENDEDOR")
        vendedores = visualizarVendedores()
        for vendedor in vendedores:
            print(f"\nNome_vendedor: {vendedor.get('nome')} \nEmail: {vendedor.get('email')} \nCPF: {vendedor.get('cpf')}")
    elif acao == 3:
        email = input("Digite o email do vendedor que deseja visualizar: ")
        visualizarVendedor(email)
        print("\nVENDEDOR ESCOLHIDO")
        print(f"\nNome_vendedor: {vendedor.get('nome')} \nEmail: {vendedor.get('email')} \nCPF: {vendedor.get('cpf')}")
    elif acao == 4:
        print("\nATUALIZAR \nVENDEDORES:")
        listarEmailsVendedores()
        email = input("Digite o email do vendedor que deseja atualizar: ")
        atualizarVendedor(email)
        print('\n Vendedor atualizado com sucesso!')
    elif  acao == 5:
        print("\nDELETAR")
        email = input("Digite o email do vendedor que deseja deletar: ")
        deletarVendedor(email)
        print(f'\n Vendedor deletado com sucesso!')
    
    if acao != 0:
        menuVendedor()


def listarEmailsVendedores():
    vendedores = visualizarVendedores()
    for vendedor in vendedores:
        print(vendedor.get('email'))
        

def inserirVendedor():
    global mydb
    nome = input("Digite o nome completo do vendedor: ")
    email = input("Digite o email: ")
    cpf = input("Digite o CPF: ")
    mydict = {"nome_vendedor": nome, "email": email, "cpf": cpf}
    mycol = mydb.vendedor
    return mycol.insert_one(mydict)


def visualizarVendedores():
    global mydb
    mycol = mydb.vendedor
    return mycol.find()


def visualizarVendedor(email):
    global mydb
    mycol = mydb.vendedor
    myquery = { "email": email }
    return mycol.find_one(myquery)


def atualizarVendedor(email):
    global mydb
    mycol = mydb.vendedor
    novoNome = input("\nDigite o novo nome do vendedor")
    novoEmail = input("Digite o novo email: ")
    novoCpf = input("Digite o novo CPF: ")
    novosValores = { "nome_vendedor": novoNome, "email": novoEmail, "cpf": novoCpf }
    return mycol.update_one({"email": email}, { "$set": novosValores})


def deletarVendedor(email):
    global mydb
    mycol = mydb.vendedor
    myquery = { "email": email }
    return mycol.delete_one(myquery)
    