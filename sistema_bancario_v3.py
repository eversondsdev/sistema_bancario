# Implementação de POO no projeto

from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Saldo insuficiente")
            return False

        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de R$ {valor:.2f} realizado com sucesso")
            return True

        else:
            print("Valor inválido")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso")
            return True
        else:
            print("Valor inválido")
            return False

    def transferir(self, valor, conta_destino):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            conta_destino._saldo += valor
            print(f"Transferência de R$ {valor:.2f} realizada com sucesso para a conta {conta_destino.numero}")
            self.historico.adicionar_transacao(Transferencia(valor, conta_destino.numero))
            conta_destino.historico.adicionar_transacao(TransferenciaRecebida(valor, self.numero))
            return True
        elif valor > self._saldo:
            print("Saldo insuficiente para realizar a transferência.")
            return False
        else:
            print("Valor inválido para transferência.")
            return False
        
        
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("O valor do saque excede o limite")
            return False
        
        elif excedeu_saques:
            print("Número de saques excedido")
            return False

        else:
            return super().sacar(valor)
        

    def __str__(self):
        return f"""\
            Agência: {self.agencia}
            C/C: {self.numero}
            Titular: {self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "detalhes": transacao.detalhes if hasattr(transacao, 'detalhes') else None
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)

class Transferencia(Transacao):
    def __init__(self, valor, conta_destino):
        self._valor = valor
        self.detalhes = f"Transferência para conta: {conta_destino}"

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        pass

class TransferenciaRecebida(Transacao):
    def __init__(self, valor, conta_origem):
        self._valor = valor
        self.detalhes = f"Transferência recebida da conta: {conta_origem}"

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        pass

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta")
        return
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def transferir(clientes, contas):
    cpf_origem = input("Informe o CPF do cliente que irá transferir: ")
    cliente_origem = filtrar_cliente(cpf_origem, clientes)

    if not cliente_origem:
        print("Cliente de origem não encontrado.")
        return

    conta_origem = recuperar_conta_cliente(cliente_origem)
    if not conta_origem:
        return

    cpf_destino = input("Informe o CPF do cliente que irá receber: ")
    cliente_destino = filtrar_cliente(cpf_destino, clientes)

    if not cliente_destino:
        print("Cliente de destino não encontrado.")
        return

    conta_destino = recuperar_conta_cliente(cliente_destino)
    if not conta_destino:
        return

    valor = float(input("Informe o valor a ser transferido: "))

    conta_origem.transferir(valor, conta_destino)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    print("\n===========EXTRATO===========")
    transacoes = conta.historico.transacoes

    extrato = ""

    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            detalhes = f" - {transacao['detalhes']}" if transacao['detalhes'] else ""
            extrato += f"\n{transacao['tipo']}: R$ {transacao['valor']:.2f}{detalhes}"
    
    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Já existe cliente com este CPF")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("Cliente criado com sucesso")
    
    
    
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso")
    

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(str(conta))
    print("=" * 100)


def menu():
    menu = """
    ================MENU===============
    [1] Depositar
    [2] Sacar
    [3] Transferir
    [4] Extrato
    [5] Novo cliente
    [6] Nova conta
    [7] Listar contas
    [8] Sair
    ==>"""
    return input(menu)



def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            transferir(clientes, contas)

        elif opcao == "4":
            exibir_extrato(clientes)

        elif opcao == "5":
            criar_cliente(clientes)

        elif opcao == "6":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "7":
            listar_contas(contas)
        
        elif opcao == "8":
            break

        else:
            print("Opção inválida")


main()
