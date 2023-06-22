from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.util import uuid

cloud_config= {
  'secure_connect_bundle': '<</PATH/TO/>>secure-connect-mercadolivre.zip'
}
auth_provider = PlainTextAuthProvider('<<CLIENT ID>>', '<<CLIENT SECRET>>')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('mercadolivre')

row = session.execute("select release_version from system.local").one()
if row:
  print(row[0])
else:
  print("An error occurred.")

def menuVendedor():
    print("\nVENDEDORES")
    print("Escolha uma ação \n")
    print(" 1 - Adicionar vendedor \n 2 - Visualizar todos vendedores \n 3 - Visualizar vendedor \n 4 - Atualizar vendedor \n 5 - Deletar vendedor \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0, 1, 2, 3, 4, 5]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))

    if acao == 1:
        print("\nCADASTRO")
        inserirVendedor()
        print('Vendedor cadastrado com sucesso!')
    elif acao == 2:
        print("\nVENDEDORES")
        vendedores = visualizarVendedores()
        for vendedor in vendedores:
            print(f"\nNome: {vendedor.get('nome_vendedor')} \nEmail: {vendedor.get('email')} \nCPF: {vendedor.get('cpf')}")
    elif acao == 3:
        print("\nEMAILS VENDEDORES:")
        listarEmailsVendedores()
        email = input("\nDigite o email do vendedor que deseja visualizar: ")
        vendedor = visualizarVendedor(email)
        print("\nVENDEDOR ESCOLHIDO")
        print(f"\nNome: {vendedor.get('nome_vendedor')} \nEmail: {vendedor.get('email')} \nCPF: {vendedor.get('cpf')}")
    elif acao == 4:
        print("\nATUALIZAR \nEMAILS VENDEDORES:")
        listarEmailsVendedores()
        email = input("Digite o email do vendedor que deseja atualizar: ")
        atualizarVendedor(email)
        print('\nVendedor atualizado com sucesso!')
    elif acao == 5:
        print("\nDELETAR")
        print("EMAILS VENDEDORES:")
        listarEmailsVendedores()
        email = input("\nDigite o email do vendedor que deseja deletar: ")
        deletarVendedor(email)
        print('Vendedor deletado com sucesso!')

    if acao != 0:
        menuVendedor()


def listarEmailsVendedores():
    query = "SELECT email FROM vendedor"
    result = session.execute(query)
    for row in result:
        print(row.email)


def inserirVendedor():
    nome = input("Digite o nome completo do vendedor: ")
    email = input("Digite o email: ")
    cpf = input("Digite o CPF: ")
    query = f"INSERT INTO vendedor (nome_vendedor, email, cpf) VALUES ('{nome}', '{email}', '{cpf}')"
    session.execute(query)


def visualizarVendedores():
    query = "SELECT * FROM vendedor"
    result = session.execute(query)
    vendedores = []
    for row in result:
        vendedor = {
            'nome_vendedor': row.nome_vendedor,
            'email': row.email,
            'cpf': row.cpf
        }
        vendedores.append(vendedor)
    return vendedores


def visualizarVendedor(email):
    query = f"SELECT * FROM vendedor WHERE email = '{email}'"
    result = session.execute(query)
    for row in result:
        vendedor = {
            'nome_vendedor': row.nome_vendedor,
            'email': row.email,
            'cpf': row.cpf
        }
        return vendedor


def atualizarVendedor(email):
    novosValores = {}
    desejo = input("Deseja atualizar o nome? S/N ")
    if desejo == "S":
        novoNome = input("\nDigite o novo nome do vendedor: ")
        novosValores["nome_vendedor"] = novoNome
    desejo = input("Deseja atualizar o email? S/N ")
    if desejo == "S":
        novoEmail = input("Digite o novo email: ")
        novosValores["email"] = novoEmail
    desejo = input("Deseja atualizar o CPF? S/N ")
    if desejo == "S":
        novoCpf = input("Digite o novo CPF: ")
        novosValores["cpf"] = novoCpf
    query = f"UPDATE vendedor SET {', '.join([f'{col} = {val}' for col, val in novosValores.items()])} WHERE email = '{email}'"
    session.execute(query)


def adicionarProdutosVendedor(email, mydict):
    query = f"SELECT produtos FROM vendedor WHERE email = '{email}'"
    result = session.execute(query)
    produtos = []
    for row in result:
        produtos = row.produtos
    produtos.append(mydict)
    query = f"UPDATE vendedor SET produtos = {produtos} WHERE email = '{email}'"
    session.execute(query)


def deletarVendedor(email):
    query = f"DELETE FROM vendedor WHERE email = '{email}'"
    session.execute(query)

