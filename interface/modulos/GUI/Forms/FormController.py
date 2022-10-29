from modulos.FileService import FileService


class FormController:
    def __init__(self, fileService: FileService) -> None:
        self.fileService = fileService

    def savePreset(self, item, nome: str):
        pass

    def deletePreset(self, nome: str):
        pass