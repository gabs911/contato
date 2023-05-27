from tkinter import Tk
from modulos.FileService import FileService
from modulos.GUI.Forms.AccelFormGUI.AccelFormController import AccelFormController
from modulos.GUI.Forms.AccelFormGUI.AccelFormData import AccelFormData
from modulos.GUI.Forms.AccelFormGUI.AccelFormView import AccelFormView
from modulos.GUI.Forms.FormData import FormData
from modulos.GUI.Forms.FormModule import FormModule
from modulos.GUI.Forms.FormView import FormView
from util.Event import SimpleEvent


class AccelFormModule(FormModule):
    '''Modulo de criação/edição de Presets de Notas'''
    def __init__(self, fileService: FileService) -> None:
        super().__init__()
        self.controller = AccelFormController(fileService)

    def createView(self, tk: Tk, event: SimpleEvent, data: FormData = None) -> FormView:
        super().createView(tk, event, data)
        if data == None:
            data = AccelFormData()
        return AccelFormView(tk, event, data, self.controller)