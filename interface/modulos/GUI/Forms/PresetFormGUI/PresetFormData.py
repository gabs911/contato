from tkinter import StringVar
from util.logFunction import log
from modulos.GUI.Forms.FormData import FormData


class PresetFormData(FormData):
    def __init__(self, data = None) -> None:
        self.item_data = data
        self.notas = []
        self.angulo_inicial: StringVar = None
        self.name: StringVar = None

    @log
    def addNote(self, angulo: StringVar, id: StringVar) -> None:
        '''Adiciona uma nota e ângulo final para a o preset'''
        self.notas.append({
            "id":id,
            "angulo":angulo
        })
    
    @log
    def NullNote(self):
        '''Cria uma nota com valores padrões'''
        return {
            "id": StringVar(self.root, ""),
            "angulo": StringVar(self.root, "0")
        }
    
    @log
    def deleteNote(self):
        '''Remove uma nota da lista de notas'''
        self.notas.pop()
    
    @log
    def convertForView(self) -> None:
        super().convertForView()
        if self.item_data == None:
            self.angulo_inicial = StringVar(self.root, "0")
            self.name = StringVar(self.root, "")
            return

        self.notas = []
        for nota in self.item_data["notas"]:
            self.addNote(
                StringVar(self.root, nota["proximo_angulo"]),
                StringVar(self.root, nota["id"])
            )
        self.angulo_inicial = StringVar(self.root, self.item_data["angulo_inicial"])
        self.name = StringVar(self.root, self.item_data["nome"])

    @log
    def convertToSave(self):
        super().convertToSave()
        notas = []
        for nota in self.notas:
            notas.append({
                "id": nota["id"].get(),
                "proximo_angulo": int(nota["angulo"].get())
            })
        return {
            "nome": self.name.get(),
            "angulo_inicial": int(self.angulo_inicial.get()),
            "notas": notas
        }