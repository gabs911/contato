from modulos.FileService import FileService

class PresetFormController:
    def __init__(self, fileService: FileService) -> None:
        self.fileService = fileService
    
    def getNotasPossiveis(self) -> list:
        return self.fileService.getNotasPossiveis()