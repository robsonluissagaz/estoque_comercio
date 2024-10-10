import PySimpleGUI as sg
import os
import json

# Caminho para o arquivo JSON
caminho_da_pasta = os.path.join(os.path.expanduser("~"), "Documents", "Estoque")
arquivo_json = os.path.join(caminho_da_pasta, 'controle_estoque.json')

# Criando a pasta dos produtos se não existir
if not os.path.isdir(caminho_da_pasta):
    os.makedirs(caminho_da_pasta)
    sg.popup(f'Pasta do programa criada em {caminho_da_pasta}')
    # Criando o arquivo dentro da pasta
    with open(arquivo_json, 'w') as arquivo:
        dados_existentes = []
        json.dump(dados_existentes, arquivo, indent=4)
        sg.popup(f'Arquivo criado em {caminho_da_pasta}')

# Funções para manipular o estoque
def cadastrar_produto():
    layout = [
        [sg.Text('Nome do Produto'), sg.Input(key='nome_produto')],
        [sg.Text('Valor'), sg.Input(key='valor')],
        [sg.Text('Quantidade'), sg.Input(key='quantidade')],
        [sg.Button('Cadastrar'), sg.Button('Cancelar')]
    ]
    janela = sg.Window('Cadastro de Produto', layout)
    while True:
        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED or evento == 'Cancelar':
            break
        elif evento == 'Cadastrar':
            if valores['nome_produto'] and valores['valor'] and valores['quantidade']:  # Verifica se os campos não estão vazios
                with open(arquivo_json, 'r+') as arquivo:
                    dados = json.load(arquivo)
                    produto = {
                        "Produto": valores['nome_produto'].upper().strip(),
                        "Valor": float(valores['valor']),
                        "Quantidade": float(valores['quantidade'])
                    }
                    dados.append(produto)
                    arquivo.seek(0)
                    json.dump(dados, arquivo, indent=4)
                sg.popup('Produto cadastrado com sucesso!')
                break
            else:
                sg.popup('Por favor, preencha todos os campos.')
    janela.close()


def pesquisar_produto():
    # Carregar os dados do arquivo JSON
    with open(arquivo_json, 'r') as arquivo:
        dados = json.load(arquivo)

    # Criar uma lista de nomes de produtos para exibir
    lista_produtos = [produto['Produto'] for produto in dados if 'Produto' in produto]

    if not lista_produtos:
        sg.popup('Nenhum produto cadastrado.')
        return

    # Criar o layout da janela com a lista de produtos
    layout = [
        [sg.Listbox(values=lista_produtos, size=(30, 6), key='produto_selecionado')],
        [sg.Button('Selecionar'), sg.Button('Cancelar')]
    ]
    janela = sg.Window('Selecionar Produto', layout)

    while True:
        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED or evento == 'Cancelar':
            break
        elif evento == 'Selecionar':
            produto_escolhido = valores['produto_selecionado']
            if produto_escolhido:  # Verifica se algum produto foi selecionado
                produto_nome = produto_escolhido[0]  # Pega o primeiro item da seleção
                for produto in dados:
                    if 'Produto' in produto and produto['Produto'].upper() == produto_nome.upper():  # Compara em maiúsculas
                        # Exibe os dados do produto em linhas separadas
                        mensagem = (f"Produto: {produto['Produto']}\n"
                                    f"Quantidade: {produto['Quantidade']}\n"
                                    f"Valor: R$ {produto['Valor']:.2f}")
                        sg.popup(mensagem)
                        break
            else:
                sg.popup('Por favor, selecione um produto da lista.')
            break
    janela.close()


def excluir_produto():
    # Carregar os dados do arquivo JSON
    with open(arquivo_json, 'r') as arquivo:
        dados = json.load(arquivo)

    # Criar uma lista de nomes de produtos para exibir
    lista_produtos = [produto['Produto'] for produto in dados if 'Produto' in produto]

    if not lista_produtos:
        sg.popup('Nenhum produto cadastrado.')
        return

    # Criar o layout da janela com a lista de produtos
    layout = [
        [sg.Listbox(values=lista_produtos, size=(30, 6), key='produto_selecionado')],
        [sg.Button('Excluir'), sg.Button('Cancelar')]
    ]
    janela = sg.Window('Excluir Produto', layout)

    while True:
        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED or evento == 'Cancelar':
            break
        elif evento == 'Excluir':
            produto_escolhido = valores['produto_selecionado']
            if produto_escolhido:  # Verifica se algum produto foi selecionado
                produto_nome = produto_escolhido[0]  # Pega o primeiro item da seleção
                dados = [produto for produto in dados if produto['Produto'] != produto_nome]  # Exclui o produto
                with open(arquivo_json, 'w') as arquivo:
                    json.dump(dados, arquivo, indent=4)  # Atualiza o JSON
                sg.popup('Produto excluído com sucesso!')
            else:
                sg.popup('Por favor, selecione um produto da lista.')
            break
    janela.close()


def alterar_produto():
    # Carregar os dados do arquivo JSON
    with open(arquivo_json, 'r') as arquivo:
        dados = json.load(arquivo)

    # Criar uma lista de nomes de produtos para exibir
    lista_produtos = [produto['Produto'] for produto in dados if 'Produto' in produto]

    if not lista_produtos:
        sg.popup('Nenhum produto cadastrado.')
        return

    # Criar o layout da janela com a lista de produtos
    layout = [
        [sg.Listbox(values=lista_produtos, size=(30, 6), key='produto_selecionado')],
        [sg.Button('Alterar'), sg.Button('Cancelar')]
    ]
    janela = sg.Window('Alterar Produto', layout)

    while True:
        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED or evento == 'Cancelar':
            break
        elif evento == 'Alterar':
            produto_escolhido = valores['produto_selecionado']
            if produto_escolhido:  # Verifica se algum produto foi selecionado
                produto_nome = produto_escolhido[0]  # Pega o primeiro item da seleção

                # Layout para alterar as informações do produto
                for produto in dados:
                    if produto['Produto'] == produto_nome:
                        novo_nome = sg.popup_get_text('Novo Nome do Produto:', default_text=produto['Produto'])
                        novo_valor = sg.popup_get_text('Novo Valor:', default_text=str(produto['Valor']))
                        nova_quantidade = sg.popup_get_text('Nova Quantidade:', default_text=str(produto['Quantidade']))

                        produto['Produto'] = novo_nome if novo_nome else produto['Produto']
                        produto['Valor'] = float(novo_valor) if novo_valor else produto['Valor']
                        produto['Quantidade'] = float(nova_quantidade) if nova_quantidade else produto['Quantidade']

                        break

                # Atualizar o JSON
                with open(arquivo_json, 'w') as arquivo:
                    json.dump(dados, arquivo, indent=4)

                sg.popup('Produto alterado com sucesso!')
            else:
                sg.popup('Por favor, selecione um produto da lista.')
            break
    janela.close()


# Função principal para o menu
def menu():
    layout = [
        [sg.Button('Cadastrar produto')],
        [sg.Button('Pesquisar produto')],
        [sg.Button('Excluir produto')],
        [sg.Button('Alterar descrição')],
        [sg.Button('Fechar programa')]
    ]
    janela = sg.Window('Menu', layout)
    while True:
        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED or evento == 'Fechar programa':
            break
        elif evento == 'Cadastrar produto':
            cadastrar_produto()
        elif evento == 'Pesquisar produto':
            pesquisar_produto()
        elif evento == 'Excluir produto':
            excluir_produto()
        elif evento == 'Alterar descrição':
            alterar_produto()
    janela.close()


# Chamando o menu
menu()
