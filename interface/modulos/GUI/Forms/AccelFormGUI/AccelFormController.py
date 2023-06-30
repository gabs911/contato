from modulos.FileService import FileService
from modulos.GUI.Forms.FormController import FormController
from util.logFunction import log


class AccelFormController(FormController):
    def __init__(self, fileService: FileService) -> None:
        super().__init__(fileService)
    
    @log
    def savePreset(self, item, nome: str):
        super().savePreset(item, nome)
        self.fileService.saveAccelPreset(item, nome)
    
    @log
    def deletePreset(self, nome: str):
        super().deletePreset(nome)
        self.fileService.deleteAccel(nome)