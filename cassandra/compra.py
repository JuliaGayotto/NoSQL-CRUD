from usuario import visualizarUsuario, listarEmailsUsuarios
from produto import visualizarProduto, listarNomesProdutos
from vendedor import visualizarVendedor, listarEmailsVendedores
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.util import uuid

cloud_config= {
  'secure_connect_bundle': 'secure-connect-mercadolivre.zip'
}
auth_provider = PlainTextAuthProvider('ZEvbLFgKJKANTefcrHGzHDeL', ',fTfqW4l9U,KvmUG_a2X7wWruzwb58GYYadc-g36AAcvpH50Dvzc0QwxlM5MDMUwZmiR5CB5CpebL8BrTRta9XZTddUbp69pnDKwYUzG+ZgcZNOY2kZB8SllW4w7OBG6')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('mercadolivre')

row = session.execute("select release_version from system.local").one()
if row:
  print(".")
else:
  print("Ocorreu um erro")

def menuCompra():
    print("\nCOMPRAS")
    print("Escolha uma ação\n")
    print(" 1 - Adicionar compra\n 2 - Visualizar todas as compras\n 3 - Visualizar compra\n 4 - Deletar compra\n 0 - Voltar ao menu\n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0, 1, 2, 3, 4]
    
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
    elif acao == 4:
        print("\nDELETAR")
        id = input("Digite o id da compra que deseja deletar: ")
        deletarCompra(id)
        print(f'\nCompra deletada com sucesso!')

    if acao != 0:
        menuCompra()


def selecionarCompra(compra):
    print(f"\nId da compra: {compra.get('id')}")
    print(f"Data da Compra: {compra.get('data_compra')}")
    usuario = compra.get("usuario")
    print(f"Usuário:  Nome: {usuario.get('nome')}  Email: {usuario.get('email')}  CPF: {usuario.get('cpf')}")
    vendedor = compra.get("vendedor")
    print(f"Vendedor:  Nome: {vendedor.get('nome_vendedor')}  Email: {vendedor.get('email')}  CPF: {vendedor.get('cpf')}")
    produtos = compra.get('produtos')

    for produto in produtos:
        print(f"Produto:  Nome: {produto.get('nome')}\nPreço: {produto.get('preco')}\nQuantidade comprada: {produto.get('quant_comprada')}")


def inserirCompra():
    dataCompra = input("Digite a data da compra: ")
    produtos = []
    desejo = 'S'
    print("PRODUTOS")
    listarNomesProdutos()

    while desejo != "N":
        nomeProduto = input("Digite o nome do produto: ")
        quant = int(input("Digite a quantidade comprada: "))
        prod = visualizarProduto(nomeProduto)
        produto = {"id": prod.get('id'), "nome": prod.get('nome'), "preco": prod.get('preco'), "quant_comprada": quant}
        produtos.append(produto)
        desejo = input("Deseja adicionar outro produto à compra? S/N ")

        print("EMAILS VENDEDORES:")
        listarEmailsVendedores()
        emailVendedor = input("Digite o email do vendedor: ")
        vend = visualizarVendedor(emailVendedor)
        vendedor = {"nome_vendedor": vend.get('nome_vendedor'), "email": vend.get('email'), "cpf": vend.get('cpf')}
        print("EMAIL USUÁRIOS:")
        listarEmailsUsuarios()
        emailUsuario = input("Digite o email do usuário: ")
        usu = visualizarUsuario(emailUsuario)
        usuario = {"nome": usu.get('nome'), "email": usu.get('email'), "cpf": usu.get('cpf')}

        query = f"INSERT INTO compra (data_compra, usuario, produtos, vendedor) VALUES ('{dataCompra}', {usuario}, {produtos}, {vendedor})"
        session.execute(query)


def visualizarCompras():
    query = "SELECT * FROM compra"
    rows = session.execute(query)
    return rows

def visualizarCompra(id):
    query = f"SELECT * FROM compra WHERE id = {id}"
    rows = session.execute(query)
    return rows.one()

def deletarCompra(id):
    query = f"DELETE FROM compra WHERE id = {id}"
    session.execute(query)