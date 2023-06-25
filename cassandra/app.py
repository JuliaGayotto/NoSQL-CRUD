from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.util import uuid
from usuario import menuUsuario
from produto import menuProduto
from compra import menuCompra
from vendedor import menuVendedor

cloud_config= {
  'secure_connect_bundle': 'secure-connect-mercadolivre.zip'
}
auth_provider = PlainTextAuthProvider('ZEvbLFgKJKANTefcrHGzHDeL', ',fTfqW4l9U,KvmUG_a2X7wWruzwb58GYYadc-g36AAcvpH50Dvzc0QwxlM5MDMUwZmiR5CB5CpebL8BrTRta9XZTddUbp69pnDKwYUzG+ZgcZNOY2kZB8SllW4w7OBG6')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('mercadolivre')

row = session.execute("select release_version from system.local").one()
if row:
  print("Conexão realizada!")
else:
  print("Ocorreu um erro")

session.set_keyspace('mercadolivre')
session.execute("CREATE TABLE IF NOT EXISTS vendedor (id UUID PRIMARY KEY, email text, nome_vendedor text, cpf text)")
session.execute("CREATE TABLE IF NOT EXISTS usuario (id UUID PRIMARY KEY, nome TEXT, email TEXT, cpf TEXT, enderecos LIST<FROZEN<MAP<TEXT, TEXT>>>, favoritos LIST<FROZEN<MAP<TEXT, TEXT>>>)")
session.execute("CREATE TABLE IF NOT EXISTS produto (id UUID PRIMARY KEY, nome TEXT, preco FLOAT, quantidade INT, vendedor MAP<TEXT, TEXT>)")
session.execute("CREATE TABLE IF NOT EXISTS compra (id UUID PRIMARY KEY, data_compra TEXT, produtos LIST<FROZEN<MAP<TEXT, TEXT>>>, vendedor FROZEN<MAP<TEXT, TEXT>>, usuario FROZEN<MAP<TEXT, TEXT>>)")


def menuPrincipal():
    print("\n COLEÇÕES: \n 1 - Usuários \n 2 - Produtos \n 3 - Compras \n 4 - Vendedores \n 0 - Sair \n")
    colecao = int(input("Escolha uma colecao: "))
    opcoes = [0,1,2,3,4]
    while colecao not in opcoes:
        colecao = int(input("Digite o número de uma coleção válida: "))

    if colecao == 1:
       menuUsuario()
    elif colecao == 2:
        menuProduto()
    elif colecao == 3:
        menuCompra()
    elif colecao == 4:
        menuVendedor()
        
    if colecao != 0:
        menuPrincipal()


###############
menuPrincipal()