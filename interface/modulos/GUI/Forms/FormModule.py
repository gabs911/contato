from tkinter import Tk
from modulos.GUI.Forms.FormController import FormController
from modulos.GUI.Forms.FormView import FormView
from modulos.GUI.Forms.FormData import FormData
from util.Event import SimpleEvent


class FormModule:
    def __init__(self) -> None:
        pass

    def createView(self, tk: Tk, event: SimpleEvent, data: FormData) -> FormView:
        pass

    def getController(self) -> FormController:
        try:
            return self.controller
        except:
            return None