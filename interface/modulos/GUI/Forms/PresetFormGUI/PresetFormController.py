from modulos.FileService import FileService
from modulos.GUI.Forms.FormController import FormController

class PresetFormController(FormController):
    def __init__(self, fileService: FileService) -> None:
        super().__init__(fileService)
    
    def getPossibleNotes(self) -> list:
        return self.fileService.getPossibleNotes()
    
    def savePreset(self, item, nome: str):
        self.fileService.saveNotesPreset(item, nome)
    
    def deletePreset(self, nome: str):
        self.fileService.deleteNote(nome)