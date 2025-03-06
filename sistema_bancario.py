from datetime import date

menu = """
O que você deseja fazer?

[1] Depositar
[2] Sacar
[3] Tranferir
[4] Extrato
[0] Sair

=> """

saldo = 0
limite_saque = 500
limite_transferencia = 1000
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

def data_extrato():
    data_atual = date.today()
    return data_atual.strftime("%d/%m/%Y")

while True:
    opcao = input(menu)

    if opcao == "1":
        valor_deposito = input("Informe o valor do depósito:").replace(",", ".")
        valor_deposito =float(valor_deposito)

        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f"Depósito: R$ {valor_deposito:.2f}\n".replace(".", ",")
            print("Depósito realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "2":
        valor_saque = input("Informe o valor do saque: ").replace(",", ".")
        valor_saque =float(valor_saque)

        if(valor_saque > limite_saque):
            print("Operação falhou! O valor informado é maior que o limite de saque.")
        elif(numero_saques >= LIMITE_SAQUES):
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

    elif opcao == "3":
        valor_transferencia = input("Informe o valor a ser transferido: ").replace(",", ".")
        valor_transferencia = float(valor_transferencia)

        if valor_transferencia > limite_transferencia:
            print("Operação falhou! O valor informado é maior que o limite de transferência.")
        elif valor_transferencia > 0 and  valor_transferencia <= saldo:
            saldo -= valor_transferencia
            extrato += f"Transferência: R$ {valor_transferencia:.2f}\n".replace(".", ",")
            print("Transferência realizada com sucesso!")
        elif valor_transferencia > saldo:
            print("Operação falhou! Saldo insuficiente.")
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "4":
        print("\n ================= Extrato =================")
        print(data_extrato()+"\n") 
        print("\n Não há transações realizadas.\n" if extrato == "" else extrato)
        print(f"Saldo atual: R$ {saldo:.2f}".replace(".", ","))
        print("==============================================")

    elif opcao == "0":
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida! Tente novamente.")


