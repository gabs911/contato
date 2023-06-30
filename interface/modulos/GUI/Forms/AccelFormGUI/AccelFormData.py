from tkinter import IntVar, StringVar
from modulos.GUI.Forms.FormData import FormData
from util.logFunction import log


class AccelFormData(FormData):
    def __init__(self, item = None) -> None:
        super().__init__()
        self.item = item
        self.nome: StringVar
        self.nota: IntVar

    @log
    def convertToSave(self):
        return {
            "nome": self.nome.get(),
            "canal": 1,
            "nota": self.nota.get()
        }
    
    @log
    def convertForView(self):
        if self.item == None:
            self.nome = StringVar(self.root, "")
            self.nota = IntVar(self.root, 0)
            return

        self.nome = StringVar(self.root, self.item["nome"])
        self.nota = StringVar(self.root, self.item["nota"])