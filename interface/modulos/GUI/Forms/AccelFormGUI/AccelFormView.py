from tkinter import Tk
from modulos.GUI.Forms.AccelFormGUI.AccelFormController import AccelFormController
from modulos.GUI.Forms.FormData import FormData
from modulos.GUI.Forms.FormView import FormView
from util.Event import SimpleEvent

class AccelFormView(FormView):
    def __init__(self, tk: Tk, event: SimpleEvent, data: FormData, controller: AccelFormController) -> None:
        super().__init__(tk, event, data)
        self.controller = controller
    
    def construct(self) -> None:
        return super().construct()