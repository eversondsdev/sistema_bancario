
from datetime import date

def menu():
    menu = """
    O que você deseja fazer?

    [1] Depositar
    [2] Sacar
    [3] Tranferir
    [4] Extrato
    [5] Novo Usuário
    [6] Nova Conta
    [7] Listar Contas
    [0] Sair

    => """
    return input(menu)


def data_extrato():
    data_atual = date.today()
    return data_atual.strftime("%d/%m/%Y")

def depositar(saldo, valor_deposito, extrato):
    if valor_deposito > 0:
        saldo += valor_deposito
        extrato += f"Depósito: R$ {valor_deposito:.2f}\n".replace(".", ",")
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def sacar(*, valor_saque, saldo, limite_saque, limite_quantidade_saque, numero_saques, extrato):
    if(valor_saque > limite_saque):
         print("Operação falhou! O valor informado é maior que o limite de saque.")
    elif(numero_saques >= limite_quantidade_saque):   
        print("Operação falhou! Limite de saques diários atingido.")
    elif(valor_saque > saldo):
        print("Operação falhou! Saldo insuficiente.")
    elif valor_saque > 0:
        saldo -= valor_saque
        extrato += f"Saque: R$ {valor_saque:.2f}\n".replace(".", ",")
        numero_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

def transferir(saldo, valor_a_transferir, limite_transferencia, extrato):
    if valor_a_transferir > limite_transferencia:
        print("Operação falhou! O valor informado é maior que o limite de transferência.")
    elif valor_a_transferir > 0 and  valor_a_transferir <= saldo:
        saldo -= valor_a_transferir
        extrato += f"Transferência: R$ {valor_a_transferir:.2f}\n".replace(".", ",")
        print("Transferência realizada com sucesso!")
    elif valor_a_transferir > saldo:
        print("Operação falhou! Saldo insuficiente.")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def gerar_extrato(saldo, /, *, extrato):
    print("\n ================= Extrato =================")
    print(data_extrato()+"\n") 
    print("\n Não há transações realizadas.\n" if extrato == "" else extrato)
    print(f"Saldo atual: R$ {saldo:.2f}".replace(".", ","))
    print("==============================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data do seu nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    filtro_usuario = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return filtro_usuario[0] if filtro_usuario else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n Usuário não encontrado, não é possivel continuar com a operação !")

def listar_contas(contas):
    if contas == []:
        print("Não há contas cadastradas.")
    
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 50)
        print(linha)

    



def main():

    AGENCIA = "0001"
    LIMITE_QUANTIDADE_SAQUE = 3

    usuarios = []
    contas = []
    saldo = 0
    limite_saque = 500
    numero_saques = 0
    limite_transferencia = 1000
    extrato = ""

    while True:
        opcao = menu()

        if opcao == "1":
            valor_deposito = input("Informe o valor do depósito: ").replace(",", ".")
            valor_deposito = float(valor_deposito)

            saldo, extrato = depositar(saldo, valor_deposito, extrato)

        elif opcao == "2":
            valor_saque = input("Informe o valor do saque: ").replace(",", ".")
            valor_saque = float(valor_saque)

            saldo, extrato, numero_saques = sacar(
                valor_saque=valor_saque,
                saldo=saldo,
                limite_saque=limite_saque,
                limite_quantidade_saque=LIMITE_QUANTIDADE_SAQUE,
                numero_saques=numero_saques,
                extrato=extrato
            )


        elif opcao == "3":
            valor_a_transferir = input("Informe o valor a ser Tranferido: ").replace(",", ".")
            valor_a_transferir = float(valor_a_transferir)

            saldo, extrato = transferir(saldo, valor_a_transferir, limite_transferencia, extrato)

        elif opcao == "4":
            gerar_extrato(saldo, extrato=extrato)

        elif opcao == "5":
            criar_usuario(usuarios)

        elif opcao == "6":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "7":
            listar_contas(contas)
        

        elif opcao == "0":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida! Tente novamente.")


main()