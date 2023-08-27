from modulos.FileService import FileService
from modulos.GUI.Forms.FormController import FormController
from util.logFunction import log, logException

class PresetFormController(FormController):
    def __init__(self, fileService: FileService) -> None:
        super().__init__(fileService)
    
    @logException
    def getPossibleNotes(self) -> list:
        return self.fileService.getPossibleNotes()
    
    @logException
    def savePreset(self, item, nome: str):
        self.fileService.saveNotesPreset(item, nome)
    
    @logException
    def deletePreset(self, nome: str):
        self.fileService.deleteNote(nome)