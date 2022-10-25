
from tkinter import BOTTOM, Tk, Toplevel
from tkinter.ttk import Button
from modulos.GUI.Forms.FormData import FormData
from util.Event import SimpleEvent


class FormView:
    def __init__(self,tk: Tk, event: SimpleEvent, data: FormData) -> None:
        self.event = event
        self.tk = tk
        self.data = data
    
    def show(self) -> None:
        self.root = Toplevel(self.tk)
        self.root.geometry("")
        self.root.focus_set()
        self.data.root = self.root
        self.data.converteParaView()
        
        self.construct()

        self.buttonSave = Button(self.root, text="Salvar", command=self.save)
        self.buttonSave.pack(anchor='sw', side=BOTTOM)

    def construct(self) -> None:
        pass

    def save(self):
        self.event.invoke(self.data.converteParaSalvar())
        self.root.destroy()