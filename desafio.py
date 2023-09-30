def menu_principal():
    menu = """
    _____________________________________
    Bem vindo ao autoatendimento DevBank!

    [1] - Depositar
    [2] - Sacar
    [3] - Extrato
    [4] - Cadastrar Conta
    [5] - Listar Contas
    [6] - Cadastrar Usuário
    [0] - Sair
    _____________________________________

    Por favor, selecione uma das opções acima: """
    return input(menu)


def depositar(saldo, valor_deposito, extrato, /):
    if valor_deposito > 0:
        saldo += valor_deposito
        extrato += f"Depósito: + R${valor_deposito:.2f}\n"
        print("\nDepósito realizado com sucesso!")
    else:
        print("\nValor inválido!")
    return saldo, extrato


def sacar(*, saldo, valor_saque, extrato, limite, numero_saques, limite_saques):
    valor_invalido = valor_saque <= 0
    saldo_excedido = valor_saque > saldo
    numero_saques_excedido = numero_saques >= limite_saques
    valor_saque_excedido = valor_saque > limite

    if valor_invalido:
        print("\nValor inválido!")
    elif saldo_excedido:
        print("\nSaque não permitido. Saldo insuficiente!")
    elif numero_saques_excedido:
        print("\nNúmero máximo de saques excedido!")
    elif valor_saque_excedido:
        print("\nOperação não autorizada! Valor máximo permitido por saque: R$500,00.")
    else:
        saldo -= valor_saque
        numero_saques += 1
        extrato += f"Saque: - R${valor_saque:.2f}\n"
        print("\nSaque realizado com sucesso! Retire o seu dinheiro no local indicado.")
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    if not extrato:
        print("\nNão foram realizadas movimentações!\n")
        print("==========================================")
    else:
        print(extrato)
        print(f"\nSaldo disponível: R$ {saldo:.2f}")
        print("==========================================")


def buscar_usuarios(cpf, usuarios):
    filtro_usuarios = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return filtro_usuarios[0] if filtro_usuarios else None


def criar_usuario(usuarios):
    cpf = input("\nInforme o CPF (apenas números): ")
    usuario = buscar_usuarios(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário cadstrado com esse CPF!")
        return
    
    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("\nUsuário cadastrado com sucesso!")


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("\nInforme o CPF (apenas números): ")
    usuario = buscar_usuarios(cpf, usuarios)

    if usuario:
        print("\nConta cadastrada com sucesso para o usuário:")
        print(f"\nNome: {usuario['nome']} \nCPF: {usuario['cpf']}")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\nUsuário não encontrado!")


def listar_contas(contas):
    if not contas:
        print("\nNão existem contas cadastradas!")
    else:
        print("_" * 40)
        for conta in contas:
            print(f"\nAgência:\t{conta['agencia']} \nC/C:\t\t{conta['numero_conta']} \nTitular:\t{conta['usuario']['nome']}")
            print("_" * 40)


def main():

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    while(True):
        opcao = menu_principal()

        if opcao == "1":
            valor_deposito = float(input("\nInforme o valor que deseja depositar: R$"))

            saldo, extrato = depositar(saldo, valor_deposito, extrato)
        
        elif opcao == "2":
            valor_saque = float(input("\nInforme o valor que deseja sacar: R$"))

            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor_saque=valor_saque,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == "4":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "6":
            criar_usuario(usuarios)

        elif opcao == "0":
            print("\nObrigado por utilizar nosso autoatendimento. Até logo! \n")
            break

        else:
            print("\nOpção inválida!")

main()
