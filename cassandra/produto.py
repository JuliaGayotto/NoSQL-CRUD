from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from vendedor import visualizarVendedor, listarEmailsVendedores
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

def menuProduto():
    print("\nPRODUTOS")
    print("Escolha uma ação \n")
    print(" 1 - Adicionar produto \n 2 - Visualizar todos produtos \n 3 - Visualizar produto \n 4 - Atualizar produto \n 5 - Deletar produto \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0, 1, 2, 3, 4, 5]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))

    if acao == 1:
        print("\nCADASTRO")
        listarEmailsVendedores()
        email = input("Digite o email do vendedor do produto que deseja cadastrar: ")
        inserirProduto(email)
        print('Produto cadastrado com sucesso!')
    elif acao == 2:
        print("\nPRODUTOS")
        produtos = visualizarProdutos()
        for produto in produtos:
            print(f"\nNome: {produto.nome} \nPreço: {round(produto.preco, 2)} \nQuantidade: {produto.quantidade} \nVendedor: {produto.vendedor.get('nome_vendedor')}")
    elif acao == 3:
        print("\nPRODUTOS:")
        listarNomesProdutos()
        nome = input("\nDigite o nome do produto que deseja visualizar: ")
        produto = visualizarProduto(nome)
        print("\nPRODUTO ESCOLHIDO")
        print(f"\nNome: {produto.nome} \nPreço: {round(produto.preco, 2)} \nQuantidade: {produto.quantidade} \nVendedor: {produto.vendedor.get('nome_vendedor')}")
    elif  acao == 4:
        print("\nATUALIZAR \nPRODUTOS:")
        listarNomesProdutos()
        nome = input("\nDigite o nome do produto que deseja atualizar: ")
        atualizarProduto(nome)
        print('Produto atualizado com sucesso!')
    elif  acao == 5:
        print("\nDELETAR")
        print("\nPRODUTOS:")
        listarNomesProdutos()
        nome = input("\nDigite o nome do produto que deseja deletar: ")
        deletarProduto(nome) 
        print('Produto deletado com sucesso!')       

    if acao != 0:
        menuProduto()

def listarNomesProdutos():
    query = "SELECT nome FROM produto"
    result = session.execute(query)
    for row in result:
        print(row.nome)


def inserirProduto(email):
    vend = visualizarVendedor(email)
    vendedor = {"id":  str(vend['id']), "nome_vendedor": vend['nome_vendedor'], "email": vend['email'], "cpf": vend['cpf']}
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preço (XX.XX): R$ "))
    quantidade = int(input("Digite a quantidade do produto: "))
    query = f"INSERT INTO produto (id, nome, preco, quantidade, vendedor) VALUES ({uuid.uuid4()}, '{nome}', {preco}, {quantidade}, {vendedor})"
    session.execute(query)


def visualizarProdutos():
    rows = session.execute("SELECT * FROM produto")
    return rows


def visualizarProduto(nome):
    query = f"SELECT * FROM produto WHERE nome = '{nome}' ALLOW FILTERING"
    rows = session.execute(query)
    return rows.one()


def atualizarProduto(nome):
    query_busca_id = f"SELECT id FROM produto WHERE nome = '{nome}'  ALLOW FILTERING"
    result = session.execute(query_busca_id)
    produto_id = result.one()[0] 
    novosValores = {}
    desejo = input("Deseja atualizar o nome? S/N ")
    if desejo == "S":
        novoNome = input("Digite o novo nome do produto: ")
        session.execute("UPDATE produto SET nome = %s WHERE id = %s", (novoNome, produto_id))
    desejo = input("Deseja atualizar o preço? S/N ")
    if desejo == "S":
        novoPreco = float(input("Digite o novo preço do produto (XX.XX): R$"))
        session.execute("UPDATE produto SET preco = %s WHERE id = %s", (novoPreco, produto_id))
    desejo = input("Deseja atualizar a quantidade em estoque? S/N ")
    if desejo == "S":
        novaQuantidade = int(input("Digite a nova quantidade: "))
        session.execute("UPDATE produto SET quantidade = %s WHERE id = %s", (novaQuantidade, produto_id))
      

def deletarProduto(nome):
    query_busca_id = f"SELECT id FROM produto WHERE nome = '{nome}'  ALLOW FILTERING"
    result = session.execute(query_busca_id)
    produto_id = result.one()[0]  
    query_exclusao = f"DELETE FROM produto WHERE id = {produto_id}"
    session.execute(query_exclusao)
    