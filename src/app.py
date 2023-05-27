from usuario import menuUsuario
from produto import menuProduto
from compra import menuCompra
from vendedor import menuVendedor

def menuPrincipal():
    print("\n COLEÇÕES: \n 1 - Usuários \n 2 - Produto \n 3 - Compra \n 4 - Vendedor \n 0 - Sair \n")
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
