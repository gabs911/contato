from tkinter import Tk
from modulos.FileService import FileService
from modulos.GUI.PresetFormGUI.PresetFormController import PresetFormController
from modulos.GUI.PresetFormGUI.PresetFormView import PresetFormView
from modulos.GUI.PresetFormGUI.PresetFormData import PresetFormData
from util.Event import SimpleEvent


class PresetFormModule:
    def __init__(self) -> None:
        self.controller = PresetFormController(FileService())

    def createView(self, tk: Tk, event: SimpleEvent, data: PresetFormData = None) -> PresetFormView:
        if data == None:
            data = PresetFormData()
        return PresetFormView(tk, event, self.controller, data)