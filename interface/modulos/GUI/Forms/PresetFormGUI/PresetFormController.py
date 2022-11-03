from modulos.FileService import FileService
from modulos.GUI.Forms.FormController import FormController

class PresetFormController(FormController):
    def __init__(self, fileService: FileService) -> None:
        super().__init__(fileService)
    
    def getNotasPossiveis(self) -> list:
        return self.fileService.getNotasPossiveis()
    
    def savePreset(self, item, nome: str):
        self.fileService.savePresetDeNotas(item, nome)
    
    def deletePreset(self, nome: str):
        self.fileService.deleteNota(nome)