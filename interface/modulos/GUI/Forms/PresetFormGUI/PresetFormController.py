from modulos.FileService import FileService
from modulos.GUI.Forms.FormController import FormController
from util.logFunction import log

class PresetFormController(FormController):
    def __init__(self, fileService: FileService) -> None:
        super().__init__(fileService)
    
    @log
    def getPossibleNotes(self) -> list:
        return self.fileService.getPossibleNotes()
    
    @log
    def savePreset(self, item, nome: str):
        self.fileService.saveNotesPreset(item, nome)
    
    @log
    def deletePreset(self, nome: str):
        self.fileService.deleteNote(nome)