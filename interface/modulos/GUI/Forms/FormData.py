from tkinter import Toplevel


class FormData:
    '''Esqueleto para o controlador do módulo de criação/edição de presets'''
    def __init__(self) -> None:
        self.root: Toplevel = None

    def convertForView(self):
        '''Converte os dados do Preset para o formato utilizado na janela de edição de preset'''
        pass
    
    def convertToSave(self):
        '''Converte os dados da interface de criação/edição de presets para o formato usado para salvar'''
        pass