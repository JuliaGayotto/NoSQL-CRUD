def update_usuario(email,novo):
    global mydb
    mycol = mydb.usuarios
    mycol.update_one({"email": email}, {"$set": novo})

def update_usuario_favoritos(email,favoritos):
    global mydb
    mycol = mydb.usuarios
    mycol.update_one({"email": email}, {"$set": {"favoritos": favoritos}})

def json_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, Decimal128):
        return str(obj.to_decimal())
    else:
        return json.JSONEncoder().default(obj)

def devolver_mongo():
    verificador()
    global chaves_alteracoes
    if chaves_alteracoes != '':
        for chave in chaves_alteracoes:
            if "s" == str(input(f"Você aceita salvar definitivamente a chave {chave}? (s/n) ")):
                ObjDevolver = json.loads(conR.get(chave))
                separacao = chave.split(":")
                if separacao[1] == "usuario":
                    update_usuario(separacao[0],ObjDevolver)
                elif separacao[1] == "favoritos":
                    produtosNome = ObjDevolver
                    produtoAdc = []
                    produtos = find_produtos()
                    for produto in produtos:
                        for produtoNome in produtosNome:
                            if (produto.get("nome") == produtoNome):
                                produtoAdc.append(produto)
                    update_usuario_favoritos(separacao[0],produtoAdc)
        print("Salvo com sucesso!")
    else:
        print("Salve algo no redis antes!")
    chaves_alteracoes = ''
    print("")
    opcoes_usuario()

def salvar_redis(emailI, valores, tipo):
    StringObjeto = json.dumps(valores,  default=json_serializer)
    conR.set(f'{emailI}:{tipo}', StringObjeto, ex=60)
    global chaves_alteracoes
    chaves_alteracoes = []
    chaves_alteracoes.append(f'{emailI}:{tipo}')
    print("Salvo no redis!")
    print("")
    opcoes_usuario()

def atualizar_cliente():
    global chaves_alteracoes
    verificador()
    emailI = input("Email do usuário à atualizar: ")
    print("Quais campos irá atualizar?")
    print("01 - Nome")
    print("02 - Sobrenome")
    print("03 - Email")
    campos = input("Quais os campos? *modelo: 01,02,03: ")
    campos = campos.split(",")
    novosValores = {}
    for campo in campos:
        campo = int(campo)
        if(campo == 1):
            nome = input("Novo nome: ")
            novosValores["nome"] = nome

        elif(campo == 2):
            sobrenome = input("Novo sobrenome: ")
            novosValores["sobrenome"] = sobrenome 

        elif(campo == 3):
            email = input("Novo email: ")
            novosValores["email"] = email
    salvar_redis(emailI, novosValores, "usuario")

def cadastrar_favoritos():
    email = input("Email do usuário: ")
    print('')
    print("Produtos disponíveis:")
    pega_produtos()
    produtosNome = []
    chave = True
    while chave:
        produtoNome = input("Nome do produto favoritado: ")
        produtosNome.append(produtoNome)
        chave = (input("Deseja adicionar outro produto? (s/n): ") == 's')
    salvar_redis(email, produtosNome, "favoritos")
