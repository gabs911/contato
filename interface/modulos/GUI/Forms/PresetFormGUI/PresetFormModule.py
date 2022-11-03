from tkinter import Tk
from modulos.FileService import FileService
from modulos.GUI.Forms.FormController import FormController
from modulos.GUI.Forms.FormModule import FormModule
from modulos.GUI.Forms.PresetFormGUI.PresetFormController import PresetFormController
from modulos.GUI.Forms.PresetFormGUI.PresetFormView import PresetFormView
from modulos.GUI.Forms.PresetFormGUI.PresetFormData import PresetFormData
from util.Event import SimpleEvent


class PresetFormModule(FormModule):
    def __init__(self) -> None:
        self.controller = PresetFormController(FileService())

    def createView(self, tk: Tk, event: SimpleEvent, data: PresetFormData = None) -> PresetFormView:
        if data == None:
            data = PresetFormData()
        return PresetFormView(tk, event, self.controller, data)