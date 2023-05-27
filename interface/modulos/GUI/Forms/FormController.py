from modulos.FileService import FileService


class FormController:
    '''Esqueleto para o controlador do módulo de criação/edição de presets'''
    def __init__(self, fileService: FileService) -> None:
        self.fileService = fileService

    def savePreset(self, item, nome: str):
        '''Salva o preset'''
        pass

    def deletePreset(self, nome: str):
        '''Deleta o preset'''
        pass