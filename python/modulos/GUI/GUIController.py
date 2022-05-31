import json
from tkinter import Tk
from modulos.EletronicModule import BaseEletronicModule
from modulos.GUI.GUIView import GUIView


class GUIController:
    def __init__(self, eletronicModule: BaseEletronicModule) -> None:
        self.eletronicModule = eletronicModule
        self.scheduler = " "
    
    RESOURCE_LOCATION = "resources/presets/notas/"
    
    NAMES = ["teste.json", "teste2.json", "teste3.json"]

    def view(self) -> GUIView:
        return GUIView(self)
    
    def getAccelPresets(self) -> list[int]:
        return [1,2,3]

    def getNotePresets(self) -> list:
        note_list = []
        for name in self.NAMES:
            with open(self.RESOURCE_LOCATION + name) as jsonfile:
                note_list.append(json.load(jsonfile))
        return note_list

    def process(self):
        pass

    def start(self, tk: Tk):
        self.scheduler = tk.after(2000, self.process)
        self.tk = tk
    
    def end(self):
        self.tk.after_cancel(self.scheduler)


