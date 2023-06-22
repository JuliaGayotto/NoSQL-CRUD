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

session.execute("CREATE KEYSPACE IF NOT EXISTS mercadolivre WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }")
session.set_keyspace('mercadolivre')
session.execute("CREATE TABLE IF NOT EXISTS vendedor (id UUID PRIMARY KEY, email text, nome_vendedor text, cpf text, produtos list<text>)")
session.execute("CREATE TABLE IF NOT EXISTS usuario (id UUID PRIMARY KEY, nome TEXT, email TEXT, cpf TEXT, enderecos LIST<FROZEN<MAP<TEXT, TEXT>>>, favoritos LIST<FROZEN<MAP<TEXT, TEXT>>>)")
session.execute("CREATE TABLE IF NOT EXISTS produto (id UUID PRIMARY KEY, nome TEXT, preco FLOAT, quantidade INT)")
session.execute("CREATE TABLE IF NOT EXISTS compra (id UUID PRIMARY KEY, data_compra TEXT, usuario MAP<TEXT, TEXT>, produtos LIST<MAP<TEXT, TEXT>>, vendedor MAP<TEXT, TEXT>)")