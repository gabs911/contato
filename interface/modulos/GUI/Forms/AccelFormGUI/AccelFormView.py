from tkinter import Frame, Tk
from tkinter.ttk import Entry, Label
from modulos.GUI.Forms.AccelFormGUI.AccelFormController import AccelFormController
from modulos.GUI.Forms.AccelFormGUI.AccelFormData import AccelFormData
from modulos.GUI.Forms.FormData import FormData
from modulos.GUI.Forms.FormView import FormView
from util.Event import SimpleEvent

class AccelFormView(FormView):
    def __init__(self, tk: Tk, event: SimpleEvent, data: FormData, controller: AccelFormController) -> None:
        super().__init__(tk, event, data)
        self.controller = controller
        self.data: AccelFormData
    
    def construct(self) -> None:
        super().construct()
        frame = Frame(self.root)
        frame.pack()

        # nome
        nomeLabel = Label(frame, text="nome")
        nomeLabel.grid(row=0, column=0)
        nomeEntry = Entry(frame, textvariable=self.data.nome)
        nomeEntry.grid(row=0, column=1)

        # nota
        notaLabel = Label(frame, text="Valor MIDI")
        notaLabel.grid(row=1, column=0)
        notaEntry = Entry(frame, textvariable=self.data.nota)
        notaEntry.grid(row=1, column=1)



