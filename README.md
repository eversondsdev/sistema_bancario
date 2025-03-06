# Sistema Bancário Simples

Este é um sistema bancário simples desenvolvido em Python, permitindo ao usuário realizar operações bancárias como depósito, saque, transferência, consulta de extrato, além de funcionalidades adicionais como criação de usuários e contas bancárias.

## Funcionalidades

- **Depósito**: O usuário pode adicionar saldo informando um valor positivo.
- **Saque**: O usuário pode sacar um valor desde que tenha saldo suficiente, respeitando o limite de saque por operação e o limite diário de saques.
- **Transferência**: O usuário pode transferir valores dentro do limite estabelecido e desde que tenha saldo suficiente.
- **Extrato**: Exibe todas as transações realizadas, juntamente com a data atual e o saldo atual da conta.
- **Criação** de Usuário: Usuários podem ser cadastrados informando nome, CPF, data de nascimento e endereço.
- **Criação de Conta Bancária**: Vincula uma conta bancária a um usuário existente.
- **Listagem de Contas**: Exibe todas as contas bancárias cadastradas no sistema

## Requisitos

- Python 3.x instalado.
- Editor de código (vscode, PyCharm).

## Como Executar

1. Clone este repositório ou copie o código para um arquivo local.
2. Execute o script no terminal ou prompt de comando:
   ```bash
   python nome_do_arquivo.py
   ```
3. Siga as instruções exibidas no menu interativo.

## Melhorias na Versão 2

- O código foi modularizado, separando as funcionalidades em funções para melhor organização e reutilização.
- Adicionada a funcionalidade de criação e gerenciamento de usuários e contas.
- Implementado limite de transferência para maior controle financeiro.
- Melhorias na exibição do extrato, incluindo a data das transações.

  
## Melhorias Futuras

- Implementação de persistência de dados com banco de dados ou arquivos.
- Interface gráfica para facilitar o uso.
- Autenticação de usuários.

## Autor

Desenvolvido por Daniel durante o Bootcamp Python Developer - Suzano, Ministrado pelo professor Guilherme Arthur de Carvalho.


