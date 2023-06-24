from produto import visualizarProdutos, visualizarProduto, listarNomesProdutos
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

def menuUsuario():
    print("\n\nUSUÁRIOS")
    print("Escolha uma ação: \n")
    print(" 1 - Adicionar usuário \n 2 - Visualizar todos usuários \n 3 - Visualizar usuário \n 4 - Atualizar usuário \n 5 - Adicionar favoritos \n 6 - Deletar usuário \n 0 - Voltar ao menu \n")
    acao = int(input("Escolha uma acao: "))
    opcoes = [0, 1, 2, 3, 4, 5, 6]
    while acao not in opcoes:
        acao = int(input("Digite o número de uma ação válida: "))

    if acao == 1:
        print("\nCADASTRO")
        inserirUsuario()
        print(f'\nUsuário cadastrado com sucesso!')
    elif acao == 2:
        print("\nUSUÁRIOS", end="")
        usuarios = visualizarUsuarios()
        for usuario in usuarios:
            selecionarUsuario(usuario)
    elif acao == 3:
        print("\nEMAIL USUÁRIOS:")
        listarEmailsUsuarios()
        email = input("\nDigite o email do usuario que deseja visualizar: ")
        usuario = visualizarUsuario(email)
        print("\nUSUÁRIO ESCOLHIDO", end='')
        selecionarUsuario(usuario)
    elif  acao == 4:
        print("\nATUALIZAR \nEMAIL USUÁRIOS:")
        listarEmailsUsuarios()
        email = input("\nDigite o email cadastrado do usuario que deseja atualizar: ")
        atualizarUsuario(email)
        print('\nUsuário atualizado com sucesso!')
    elif  acao == 5:
        print("\nADICIONAR FAVORITOS \nEMAIL USUÁRIOS:")
        listarEmailsUsuarios()
        email = input("\nDigite o email do usuário em que se deseja adicionar favorito(s): ")
        adicionarFavoritos(email)
        print('Favorito adicionado com sucesso!')
    elif  acao == 6:
        print("\nDELETAR \nEMAIL USUÁRIOS:")
        listarEmailsUsuarios()
        email = input("\nDigite o email do usuário que deseja deletar: ")
        deletarUsuario(email)
        print(f'\nUsuário deletado com sucesso!')

    if acao != 0:
        menuUsuario()


def listarEmailsUsuarios():
    usuarios = visualizarUsuarios()
    for usuario in usuarios:
        print(usuario.email)


def selecionarUsuario(usuario):
    print(f"\n\nNome: {usuario.nome} \nEmail: {usuario.email} \nCPF: {usuario.cpf}", end='')       
    enderecos = usuario.enderecos
    for endereco in enderecos:
        cep = endereco['cep']
        numero = endereco['numero']
        complemento = endereco['complemento']
        print(f"\nENDEREÇO: \nCEP: {cep}  Número: {numero} ", end='')
        if complemento:
            print(f"Complemento: {complemento}", end='')
    favoritos = usuario.favoritos
    if favoritos:
        for favorito in favoritos:
            nome = favorito['nome_favorito']
            preco = favorito['preco']
            preco_arredondado = "{:.2f}".format(round(float(preco), 2))
            print(f"\nFAVORITO: Nome: {nome}  Preço: R${preco_arredondado}", end='')

def inserirUsuario():
    nome = input("Digite o nome completo do usuário: ")
    email = input("Digite o email: ")
    cpf = input("Digite o CPF: ")
    enderecos = []
    repetir = 'S'

    while repetir != "N":
        cep = input("Digite o CEP: ")
        num = input("Digite o número: ")
        desejo = input("Deseja adicionar um complemento? S/N ")
        if desejo == "S":
            complemento = input("Digite o complemento: ")
        else:
            complemento = ''
        end = {"cep": cep, "numero": num, "complemento": complemento}
        enderecos.append(end)
        repetir = input("Digitar outro endereço (S/N)? ")

    query = f"INSERT INTO usuario (id, nome, email, cpf, enderecos) VALUES ({uuid.uuid4()}, '{nome}', '{email}', '{cpf}', {enderecos})"
    session.execute(query)

def visualizarUsuarios():
    query = "SELECT * FROM usuario"
    result = session.execute(query)
    return result

def visualizarUsuario(email):
    query = f"SELECT * FROM usuario WHERE email = '{email}' ALLOW FILTERING"
    result = session.execute(query)
    return result.one()


def atualizarUsuario(email):
    query_busca_id = f"SELECT id FROM usuario WHERE email = '{email}'  ALLOW FILTERING"
    result = session.execute(query_busca_id)
    usuario_id = result.one()[0] 

    novosValores = {}
    desejo = input("Deseja atualizar o nome? S/N ")
    if desejo == "S":
        novoNome = input("\nDigite o novo nome do usuário: ")
        session.execute("UPDATE usuario SET nome = %s WHERE id = %s", (novoNome, usuario_id))
    desejo = input("Deseja atualizar o email? S/N ")
    if desejo == "S":
        novoEmail = input("Digite o novo email: ")
        session.execute("UPDATE usuario SET email = %s WHERE id = %s", (novoEmail, usuario_id))
    desejo = input("Deseja atualizar o CPF? S/N ")
    if desejo == "S":
        novoCpf = input("Digite o novo CPF: ")
        session.execute("UPDATE usuario SET cpf = %s WHERE id = %s", (novoCpf, usuario_id))

    enderecos = []
    repetir = 'S'
    desejo = input("Deseja atualizar o endereço? S/N ")
    if desejo == "S":
        while repetir != "N":
            cep = input("Digite o CEP: ")
            num = input("Digite o número: ")
            desejo = input("Possui complemento? S/N ")
            if desejo == "S":
                complemento = input("Digite o complemento: ")
            else:
                complemento = ''
            end = {"cep": cep, "numero": num, "complemento": complemento}
            enderecos.append(end)
            repetir = input("Digitar outro endereço (S/N)? ")
        session.execute("UPDATE usuario SET enderecos = %s WHERE id = %s", (enderecos, usuario_id))


def adicionarFavoritos(email):
    query_busca_id = f"SELECT id FROM usuario WHERE email = '{email}'  ALLOW FILTERING"
    result = session.execute(query_busca_id)
    usuario_id = result.one()[0] 
    favoritos = []
    usu = visualizarUsuario(email)
    try:
        for favorito in usu.getFavoritos:
            favoritos.append(favorito)
    except:
        print()
    desejo = "S"
    while desejo != "N":
        print("PRODUTOS")
        listarNomesProdutos()
        favorito = input("Digite o nome do produto que deseja favoritar: ")
        produtoFavoritado = visualizarProduto(favorito)
        favorito = {"id": str(produtoFavoritado.id), "nome_favorito": str(produtoFavoritado.nome), "preco": str(produtoFavoritado.preco)}
        favoritos.append(favorito)
        desejo = input("Deseja adicionar outro produto em favoritos? S/N ")

    update_query = f"UPDATE usuario SET favoritos = {favoritos} WHERE id = {usuario_id}"
    session.execute(update_query)

def deletarUsuario(email):
    query_busca_id = f"SELECT id FROM usuario WHERE email = '{email}'  ALLOW FILTERING"
    result = session.execute(query_busca_id)
    usuario_id = result.one()[0]  
    query_exclusao = f"DELETE FROM usuario WHERE id = {usuario_id}"
    session.execute(query_exclusao)
