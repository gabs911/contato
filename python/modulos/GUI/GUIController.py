import json
from tkinter import Tk
from modulos.EletronicModule import BaseEletronicModule


class GUIController:
    def __init__(self, eletronicModule: BaseEletronicModule) -> None:
        self.eletronicModule = eletronicModule
        self.scheduler = ""
    
    RESOURCE_LOCATION = "resources/presets/notas/"
    
    NAMES = ["teste.json", "teste2.json", "teste3.json"]
    
    def getAccelPresets(self) -> list[int]:
        return [1,2,3]

    def getNotePresets(self) -> list:
        note_list = []
        for name in self.NAMES:
            with open(self.RESOURCE_LOCATION + name) as jsonfile:
                note_list.append(json.load(jsonfile))
        return note_list

    def start(self, tk: Tk, GUIData):
        self.GUIData = GUIData
        self.scheduler = tk.after(10, self.process)
        self.tk = tk
    
    def end(self):
        self.tk.after_cancel(self.scheduler)

    def process(self):
        '''@private - Função para uso interno do GUIController'''
        eletronicData = self.eletronicModule.getData()
        canal = self.selectCanal(self.GUIData, eletronicData)
        nota = self.selectNota(self.GUIData, eletronicData)
        on = self.selectOn(self.GUIData, eletronicData)
        if(nota is not None):
            self.send(canal, nota, on)
        else:
            print("no note")
        #pode aumentar o intervalo para testar com o Mock
        self.scheduler = self.tk.after(10, self.process)

    def selectCanal(self, GUIData, eletronicData):
        return ""
    
    def selectNota(self, GUIData, eletronicData):
        preset = GUIData["preset"]
        giro = eletronicData["giroscopio"]
        if (giro <= preset["angulo_inicial"]):
            return None
        for nota in preset["notas"]:
            if giro <= nota["proximo_angulo"]:
                return nota["id"]
        return None

    def selectOn(self, GUIData, eletronicData):
        return True

    def send(self, canal, nota: str, on = False):
        '''
        Envia a informação para o Midiout
        :param 1 canal: canal em que será enviada a nota
        :param 2 nota: nota a ser tocada
        :param 3 on: Se é para iniciar ou parar uma nota: True - > liga, False -> desliga
        '''
        conversor = { "C": 60, "D": 62, "E": 64, "F": 65, "G": 67}

        print(f"canal: {canal}\nnota: {nota}\non: {on}")
        print("-----------------------------------------------------")


