import json
from tkinter import Tk
from modulos.EletronicModule import BaseEletronicModule
from modulos.FileService import FileService
from modulos.MidiService import MidiService


class GUIController:
    def __init__(self, eletronicModule: BaseEletronicModule, midiService: MidiService) -> None:
        self.eletronicModule = eletronicModule
        self.scheduler = ""
        self.midiService = midiService
        self.permite_accel = True
        self.permite_nota = { "A": True, "B": True, "C": True, "D": True, "E": True, "F": True, "G": True }
        self.fileService = FileService()
  
    def getAccelPresets(self) -> list:
        return self.fileService.getAccelPresets()

    def getNotePresets(self) -> list:
        return self.fileService.getNotePresets()

    INTERVALO_DE_CHECAGEM = 1
    def start(self, tk: Tk, GUIData):
        self.GUIData = GUIData
        self.scheduler = tk.after(self.INTERVALO_DE_CHECAGEM, self.process)
        self.tk = tk
    
    def end(self):
        self.tk.after_cancel(self.scheduler)

    def process(self):
        '''@private - Função para uso interno do GUIController'''
        eletronicData = self.eletronicModule.getData()
        print(eletronicData)
        if(eletronicData != None):
            self.processToque(eletronicData)
            self.processAccel(eletronicData)
        # pode aumentar o intervalo para testar com o Mock
        self.scheduler = self.tk.after(self.INTERVALO_DE_CHECAGEM, self.process) # chama a si mesmo depois de um determinado período de tempo
    
    TOUCH_NOTE_VELOCITY = 100
    def processToque(self, eletronicData):
        TOQUE_NOTE_DURATION = 200 # em milisegundos
        CANAL = 0
        nota = self.selecionaNota(self.GUIData, eletronicData)
        if(nota is not None) and (eletronicData["toque"] < 30) and self.permite_nota[nota]:
            self.send(CANAL, nota, self.TOUCH_NOTE_VELOCITY)
            self.tk.after(TOQUE_NOTE_DURATION, lambda: self.send(CANAL, nota, self.TOUCH_NOTE_VELOCITY, False))
            self.permite_nota[nota] = False

            def setPermiteNotaTrue(self: GUIController, nota):
                self.permite_nota[nota] = True
            self.tk.after(10, lambda: setPermiteNotaTrue(self, nota))
    
    def selecionaNota(self, GUIData, eletronicData):
        preset = GUIData["preset"]
        giro = eletronicData["giroscopio"]
        if (giro <= preset["angulo_inicial"]):
            return None
        for nota in preset["notas"]:
            if giro <= nota["proximo_angulo"]:
                return nota["id"]
        return None

    ACCEL_NOTE_VELOCITY = 120
    def processAccel(self, eletronicData):
        CANAL = 1
        NOTA = "accel"
        ACCEL_NOTE_DURATION = 200 # em milisegundos
        if(eletronicData["acelerometro"] >= self.GUIData["accel"]) and self.permite_accel:
            self.send(CANAL, NOTA, self.ACCEL_NOTE_VELOCITY)
            self.tk.after(ACCEL_NOTE_DURATION, lambda: self.send(CANAL, NOTA, self.ACCEL_NOTE_VELOCITY, False))
            self.permite_accel = False

            def setPermiteAccelTrue(self: GUIController):
                self.permite_accel = True
            self.tk.after(1000, lambda: setPermiteAccelTrue(self))
    
    CONVERSOR = { "C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "accel": 78 }

    def send(self, canal: int, nota: str, velocity: int, on = True):
        '''
        Envia a informação para o Midiout
        :param 1 canal: canal em que será enviada a nota
        :param 2 nota: nota a ser tocada
        :param 3 on: Se é para iniciar ou parar uma nota: True - > liga, False -> desliga
        '''
        self.midiService.send(canal, on, self.CONVERSOR[nota], velocity)


