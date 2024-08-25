### aqui é a MAIN
import json

from datetime import datetime

# Abre o arquivo .json que contém os dados do estoque.
with open('estoque_produtos.json', 'r', encoding='utf-8') as arquivo:
    texto = arquivo.read()
    # Carrega o arquivo .json criando o dicionário "estoque".
    estoque = json.loads(texto)
    # Modifica as chaves que são str para int.
    produtos = {int(chave): valor for chave, valor in estoque.items()}

# Abre o arquivo .json que contém os dados do histórico de vendas. A lógica é a mesma do arquivo .json "estoque".
with open('historico_vendas.json', 'r', encoding='utf-8') as arquivo:
    texto = arquivo.read()
    historico = json.loads(texto)
    historico_vendas = {int(chave): valor for chave, valor in historico.items()}

vendas = {}

# Função para gerar um novo histórico de vendas atualizado, mantendo as informações antigas.
def gerar_historico_vendas(carrinho):
    # Cria a data/hora da compra.
    data_hora = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    
    # Percorre o carrinho de compras.
    for i in range(len(carrinho)):
        # A cada iteração cria uma nova chave para o histórico.
        identificador = gerar_novo_id(historico_vendas)
        # Cada venda é adicionada a uma chave única.
        historico_vendas[identificador] = {
            'nome': carrinho[i]['nome'],
            'preço': carrinho[i]['preço'],
            'quantidade': carrinho[i]['quantidade'],
            'total': carrinho[i]['total'],
            'data_hora': data_hora
        }
    # Com o dicionário contendo todas as informações antigas e também as atualizadas, é criado um novo arquivo .json com o histórico totalmente atualizado.
    with open('historico_vendas.json', 'w', encoding='utf-8') as arquivo:
        arquivo.write(json.dumps(historico_vendas))
    
    return

# Função para atualizar o estoque.
def atualizar_estoque():
    # Os arquivos .json tanto de estoque quanto de venda são transformados em dicionários para manipulação.
    with open('estoque_produtos.json', 'r', encoding='utf-8') as arquivo:
        texto = arquivo.read()
        estoque = json.loads(texto)  # "estoque" agora é um dicionário.
        
    with open('venda_atual.json', 'r', encoding='utf-8') as arquivo:
        texto = arquivo.read()
        venda = json.loads(texto)  # "venda" agora é um dicionário.

    # Itera sobre cada item do dicionário "estoque".
    for i in estoque:
        # Itera sobre cada item da venda atual.
        for item in venda:
            # Verifica se o nome do produto vendido está presente no nome do produto em estoque.
            if venda[item][0] in estoque[i]['nome']:
                # Se a condição for verdadeira, subtrai a quantidade vendida da disponível no estoque.
                estoque[i]['quantidade'] -= venda[item][2]
    # Com o dicionário "estoque" atualizado, é criado o arquivo atualizado .json.
    with open('estoque_produtos.json', 'w', encoding='utf-8') as arquivo:
        arquivo.write(json.dumps(estoque))
        
    return

# Cria um relatório da venda atual utilizado para atualizar o estoque.
def relatorio_venda_atual(carrinho):
    # Cria a data/hora.
    data_hora = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    # Percorre o número de itens no carrinho e atribui as informações no dicionário "vendas".
    for i in range(len(carrinho)):
        vendas[i] = carrinho[i]['nome'], carrinho[i]['preço'], carrinho[i]['quantidade'], carrinho[i]['total'], data_hora
    # Cria um relatório da venda atual.
    with open('venda_atual.json', 'w', encoding='utf-8') as arquivo:
        arquivo.write(json.dumps(vendas))
    
    return

# Função para verificar se o valor é menor ou igual a zero.
def verificar_identificador(valor):
    # Como o programa funciona com todas as chaves iniciando no número 1 (um),
    # além de verificar se é um número válido,
    # também verifica se o número digitado está contido dentre as chaves existentes.
    if valor <= 0 or valor > max(produtos.keys()):
        raise ValueError

# Função para verificar se a variável está vazia.
def verificar_vazio(valor):
    if valor == "":
        raise ValueError

# Função para gerar ID automaticamente no dicionário de produtos.
def gerar_novo_id(produto_ID):
    if produto_ID:
        # Gera uma nova chave e garante que todas as chaves comecem com o número 1 (um).
        return max(ID for ID in produto_ID.keys()) + 1
    else:
        return 1

# Função para verificar se o valor é menor ou igual a zero.
def verificar_preco_quantidade(valor):
    if valor <= 0:
        raise ValueError

# 1 - Função para cadastrar produtos.
def cadastrar_produto():
    print("\n--- Cadastrar novo Produto ---")
    # Gera uma nova chave e atribui à variável identificador.
    identificador = gerar_novo_id(produtos)

    # Validar nome.
    while True:
        try:
            nome = input("Digite o nome do produto: ")
            verificar_vazio(nome)
            break
        except ValueError:
            print("Erro: O nome é obrigatório e não pode estar vazio.")

    # Validar preço.
    while True:
        try:
            preco = float(input("Digite o preço do produto: "))
            verificar_preco_quantidade(preco)
            break
        except ValueError:
            print("Erro: Valor inválido. O preço deve ser informado, ser um número positivo maior que 0 e não pode conter letras.")

    # Validar quantidade.
    while True:
        try:
            quantidade = int(input("Digite a quantidade em estoque disponível: "))
            verificar_preco_quantidade(quantidade)
            break
        except ValueError:
            print("Erro: Valor inválido. A quantidade em estoque deve ser informada, ser um número positivo maior que 0 e não pode conter letras.")

    # Validar categoria.
    while True:
        try:
            categoria = input("Digite a categoria do produto: ")
            verificar_vazio(categoria)
            break
        except ValueError:
            print("Erro: A categoria é obrigatória e não pode estar vazia.")

    # A descrição pode ser opcional, então não há validação.
    descricao = input("Digite a descrição do produto (ou pressione enter se não quiser adicionar): ")
    
    with open('estoque_produtos.json', 'r', encoding='utf-8') as arquivo:
        texto = arquivo.read()
        estoque = json.loads(texto)
        # Adiciona o novo produto ao dicionário de produtos.
        estoque[identificador] = {
        "nome": nome, "preço": preco, "quantidade": quantidade, "categoria": categoria, "ativo": True
        }

        # Caso o usuário tenha digitado a descrição, ela é adicionada ao produto.
        if descricao:
            estoque[identificador]["descrição"] = descricao

    with open('estoque_produtos.json', 'w', encoding='utf-8') as arquivo:
        arquivo.write(json.dumps(estoque))

    return f"{nome} cadastrado com sucesso!"

# 2 - Função para listar todos os Produtos.
def listar_produtos(lista_produtos):
    print("\n--- Lista de Produtos ---\n")
    for chave, produto in lista_produtos.items():
        # Lista os produtos que não foram excluídos.
        if produto["ativo"] == True:
            print(chave, produto["nome"])

# 3 - Função para atualizar produtos.
def atualizar_produto():
    print("\n--- Atualização de Produto ---")
    while True:
        try:
            # Se o usuário digitar o 0 (zero), são listadas as chaves e os produtos para escolher qual produto atualizar.
            listar = input("Digite 0 para listar os Produtos disponíveis: ")
            
            if listar == "0":
                listar_produtos(produtos)

            identificador = int(input("\nDigite o número do produto que deseja atualizar: "))
            # Verifica se é um número válido e se o número está contido nos números disponíveis.
            verificar_identificador(identificador)
            # Se o produto tiver sido excluído, é informado ao usuário.
            if produtos[identificador]["ativo"] == False:
                return "\nErro: Produto não disponível."
            # Imprime as informações atuais do produto que o usuário vai atualizar.
            for chave, valor in produtos[identificador].items():
                print(f"{chave}: {valor}")
            break
        except ValueError:
            print('\nErro: Número do produto inválido. Por favor, insira um número válido para atualizar o produto desejado.\n')

    # Valida a Atualização do Preço.
    while True:
        try:
            preco = float(input("\nDigite o novo preço do produto: "))
            verificar_preco_quantidade(preco)
            break
        except ValueError:
            print("\nErro: Valor inválido. O novo preço deve ser um número positivo maior que 0 e não pode conter letras. Não utilize vírgula.")

    # Valida a Atualização da Quantidade em estoque.
    while True:
        try:
            quantidade = int(input("\nDigite a nova quantidade em estoque disponível: "))
            verificar_preco_quantidade(quantidade)
        
            with open('estoque_produtos.json', 'r', encoding='utf-8') as arquivo:
                texto = arquivo.read()
                estoque = json.loads(texto)
                estoque[identificador] = {
                    'preço': preco,
                    'quantidade': quantidade
                }
            with open('estoque_produtos.json', 'w', encoding='utf-8') as arquivo:
                arquivo.write(json.dumps(estoque))
                
            return f"\n{produtos[identificador]['nome']} atualizado com sucesso!"
        except ValueError:
            print("\nErro: Valor inválido. A quantidade em estoque deve ser um número positivo maior que 0 e não pode conter letras.")
    
# 4 - Função para excluir produtos.
def excluir_produto():
    print("\n--- Exclusão de Produto ---")
    cont = 0
    while True:
        try:
            # Contador para o caso de o usuário errar o identificador do produto 3 vezes.
            if cont == 3:
                break
            # Opção para listar ao usuário as opções disponíveis.
            listar = input("Digite 0 para visualizar os produtos para exclusão: ")
            if listar == "0":
                listar_produtos(produtos)

            identificador = int(input("Digite o identificador do produto que deseja excluir: "))
            verificar_identificador(identificador)
            # Altera o valor "ativo" para False, assim o produto não é excluído definitivamente.
            # Posteriormente, poderíamos ter um histórico de todos os produtos que já foram adicionados.
            produtos[identificador]["ativo"] = False
            return f"\n{produtos[identificador]['nome']} excluído(a) com sucesso!"
        
        except ValueError:
            cont += 1
            print("Produto não encontrado! Digite um identificador válido!")

# 5 - Função para Realização de Venda.
def realizar_venda():
    print("\n--- Realização de Venda ---")

    # Será uma lista de dicionários para armazenar as compras de diferentes produtos de uma vez só.
    carrinho = []

    while True:
        try:
            print('\n1. Visualizar Produtos disponíveis para vendas')
            print('2. Adicionar produto ao carrinho')
            print('3. Finalizar Venda')
            print('4. Voltar ao Menu Principal')
            opcao = int(input('Digite uma opção: '))

            if opcao == 1:
                listar_produtos(produtos)
            # Adiciona produtos ao carrinho de compras
            elif opcao == 2:
                cont = 0
                while True:
                    try:
                        # Contador para o caso do usuário errar o identificador do produto 3 vezes.
                        if cont == 3:
                            break
                        
                        # Valida se é um número válido e se está contido dentro dos números disponíveis
                        identificador = int(input("\nDigite o identificador do produto que deseja realizar a venda: "))
                        verificar_identificador(identificador)

                        # Caso a quantidade do produto escolhido seja 0 (zero)
                        if produtos[identificador]['quantidade'] == 0:
                            print(f"{produtos[identificador]['nome']} esgotado!")
                            break
                        # Valida se o produto já foi excluído
                        if produtos[identificador]["ativo"] == True:
                            quantidade = int(input("\nDigite a quantidade que deseja vender: "))
                            verificar_preco_quantidade(quantidade)

                            # Verifica se a quantidade disponível em estoque é suficiente para a venda.
                            if quantidade <= produtos[identificador]["quantidade"] and quantidade > 0:

                                # Atualiza a quantidade
                                produtos[identificador]["quantidade"] -= quantidade

                                # Adiciona produtos ao carrinho com informações como:
                                # nome, preço, quantidade vendida, valor total da compra do item.
                                carrinho.append({'nome': produtos[identificador]['nome'], 'preço': produtos[identificador]['preço'], 'quantidade': quantidade, 'total': produtos[identificador]['preço'] * quantidade})
                                
                                # Imprime uma mensagem confirmando que o produto foi adicionado ao carrinho
                                print(f"\n{quantidade} unidade(s) do produto {produtos[identificador]['nome']} adicionada(s) ao carrinho.\n")
                                break
                            
                            elif quantidade == 0:
                                print('Erro: A quantidade deve ser maior que 0 (zero).\n')

                            else:
                                print(f'\nQuantidade insuficiente no estoque. Temos {produtos[identificador]["quantidade"]} disponível(is).')
                        
                        else:
                            print(f"\nErro: Produto '{produtos[identificador]['nome']}' foi excluído e não pode ser vendido.")
                            break

                    except ValueError:
                        cont += 1
                        print("Produto não encontrado! Digite um identificador válido!")
            # Calcula e finaliza a Venda.
            elif opcao == 3:  
                print("\n--- Finalizando a Venda ---")

                if carrinho:
                    # Soma todos os valores dos itens adicionados ao carrinho
                    total = sum([i['total'] for i in carrinho])
                    print(f"\nVenda finalizada com sucesso! Valor total: R${total:.2f}")
                    
                    # Gera um relatório de venda atual que será utilizado para atualizar o estoque
                    relatorio_venda_atual(carrinho)
                    # Atualiza o histórico de vendas, mantendo os dados de vendas anteriores
                    gerar_historico_vendas(carrinho)
                    # Atualiza o estoque atual
                    atualizar_estoque()
                    return
                
                else:
                    print("\nO carrinho está vazio. Adicione produtos ao carrinho antes de finalizar a venda.")

            elif opcao == 4:  # Voltar ao Menu Principal.
                return

        except ValueError:
            print("\nErro: Selecione uma opção válida!")

# 6 - Função para imprimir o histórico completo de vendas na tela para o usuário.
def visu_hist_vendas():
    print("\n--- Histórico de Vendas ---")
    # Caso nunca tenha acontecido uma venda
    if historico_vendas == {}:
        print('\nAinda não foi realizada a primeira venda.')
    # Percorre o dicionário "historico_vendas" e imprime as informações tratadas na tela.
    for chave in historico_vendas:
        valor = historico_vendas[chave]
        print(f"Nome: {valor['nome']}, Preço: {valor['preço']}, Quantidade Vendida: {valor['quantidade']}, Total: {valor['total']}, Data/Hora: {valor['data_hora']}")

# Menu Principal:
def menu_principal():
    while True:                             
        print("\n--- Menu Principal ---")
        print("1. Cadastrar novo Produto")
        print("2. Listar Produtos")
        print("3. Atualizar Produto")
        print("4. Excluir Produto")
        print("5. Realizar Venda")
        print("6. Relatório de vendas")
        print("7. Sair")
        try:
            opcao = int(input("Escolha uma opção: "))

            if opcao == 1:
                print(cadastrar_produto())

            elif opcao == 2:
                listar_produtos(produtos)

            elif opcao == 3:
                print(atualizar_produto())

            elif opcao == 4:
                print(excluir_produto())

            elif opcao == 5:
                realizar_venda()

            elif opcao == 6:
                visu_hist_vendas()

            elif opcao == 7:
                print("\nSaindo do sistema... Obrigado!")
                break

            else:
                print("\nOpção inválida! Digite um número entre 1 e 7.")

        except ValueError:
            print("\nErro: Digite um número válido.")

menu_principal()
