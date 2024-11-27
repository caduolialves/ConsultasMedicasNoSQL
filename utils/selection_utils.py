from prompt_toolkit.shortcuts import radiolist_dialog

def selecionar_item(titulo, lista):
    """
    Exibe uma lista interativa para o usuário selecionar um item.
    :param titulo: Título da seleção (string)
    :param lista: Lista de itens no formato [(id, "Texto para exibir"), ...]
    :return: ID do item selecionado
    """
    resultado = radiolist_dialog(
        title=titulo,
        text="Use as setas para navegar e Enter para selecionar:",
        values=lista,
    ).run()

    return resultado
