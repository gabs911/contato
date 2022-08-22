import json
from tkinter import Tk
from modulos.GUI.GUIData import GUIButtonState
from modulos.EletronicModule import BaseEletronicModule
from modulos.FileService import FileService
from modulos.MidiService import MidiService
from modulos.GUI.GUIData import GUIData


class GUIController:
    INTERVALO_DE_CHECAGEM = 1
    TOUCH_NOTE_VELOCITY = 100

    def __init__(self, eletronicModule: BaseEletronicModule, midiService: MidiService) -> None:
        self.eletronicModule = eletronicModule
        self.scheduler = ""
        self.midiService = midiService
        self.permite_accel = True
        self.permite_nota = None
        self.fileService = FileService()
  
    def getAccelPresets(self) -> list:
        return self.fileService.getAccelPresets()

    def getNotePresets(self) -> list:
        return self.fileService.getNotePresets()

    def start(self, tk: Tk, GUIData: GUIData):
        self.eletronicModule.setup()
        self.permite_nota = dict()
        for nota in self.fileService.getNotasPossiveis():
            self.permite_nota[nota] = True
        self.GUIData = GUIData
        self.scheduler = tk.after(self.INTERVALO_DE_CHECAGEM, self.process)
        self.tk = tk
    
    def end(self):
        self.tk.after_cancel(self.scheduler)
        self.eletronicModule.teardown()

    def process(self):
        '''@private - Função para uso interno do GUIController'''
        self.GUIData.setButtonState(GUIButtonState.INICIADO)
        eletronicData = self.eletronicModule.getData()
        #print(eletronicData)
        if(eletronicData != None):
            self.processToque(eletronicData)
            self.processAccel(eletronicData)
        # pode aumentar o intervalo para testar com o Mock
        self.scheduler = self.tk.after(self.INTERVALO_DE_CHECAGEM, self.process) # chama a si mesmo depois de um determinado período de tempo
    
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
    
    def selecionaNota(self, GUIData: GUIData, eletronicData):
        preset = GUIData.getNotePreset()
        giro = eletronicData["giroscopio"]
        if (giro <= preset["angulo_inicial"]):
            return None
        for nota in preset["notas"]:
            if giro <= nota["proximo_angulo"]:
                return nota["id"]
        return None

    def processAccel(self, eletronicData):
        ACCEL_PRESET = self.GUIData.getAccelPreset()
        CANAL = ACCEL_PRESET["canal"]
        NOTA = ACCEL_PRESET["nota"]
        ACCEL_NOTE_VELOCITY = 120
        ACCEL_NOTE_DURATION = 200 # em milisegundos
        if(eletronicData["acelerometro"] >= self.GUIData.getAccel()) and self.permite_accel:
            self.send(CANAL, NOTA, ACCEL_NOTE_VELOCITY)
            self.tk.after(ACCEL_NOTE_DURATION, lambda: self.send(CANAL, NOTA, ACCEL_NOTE_VELOCITY, False))
            self.permite_accel = False

            def setPermiteAccelTrue(self: GUIController):
                self.permite_accel = True
            self.tk.after(1000, lambda: setPermiteAccelTrue(self))
    
    def converteNota(self, nota) -> int:
        if(type(nota) is str):
            return self.fileService.getConversorDeNotas()[nota]
        return nota

    def send(self, canal: int, nota, velocity: int, on = True):
        '''
        Envia a informação para o Midiout
        :param 1 canal: canal em que será enviada a nota
        :param 2 nota: nota a ser tocada
        :param 3 on: Se é para iniciar ou parar uma nota: True - > liga, False -> desliga
        '''
        self.midiService.send(canal, on, self.converteNota(nota), velocity)


