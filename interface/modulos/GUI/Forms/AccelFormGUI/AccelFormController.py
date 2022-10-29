from modulos.FileService import FileService


class AccelFormController:
    def __init__(self, fileService: FileService) -> None:
        self.fileService = fileService
    
    def savePreset(self, item, nome: str):
        self.fileService.saveAccelPreset(item, nome)