import json
from serial import SerialException
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
        self.fileService = FileService()
        self.ultimaNota = ""
  
    def getAccelPresets(self) -> list:
        return self.fileService.getAccelPresets()

    def getNotePresets(self) -> list:
        return self.fileService.getNotePresets()

    def savePresetDeNotas(self, item, nome: str) -> None:
        self.fileService.savePresetDeNotas(item, nome)

    def listCOMPorts(self):
        return self.eletronicModule.listCOMPorts()

    def listMIDIPorts(self):
        return self.midiService.listMIDIPorts()

    def start(self, tk: Tk, GUIData: GUIData):
        self.GUIData = GUIData
        self.scheduler = tk.after(self.INTERVALO_DE_CHECAGEM, self.process)
        self.tk = tk
        try:
            self.midiService.setup(int(self.GUIData.MIDIText.get().split(" ")[-1]))
            self.eletronicModule.setup(self.GUIData.COMText.get())
            self.GUIData.setButtonState(GUIButtonState.INICIADO)
            print("Start")
        except SerialException:
            self.GUIData.setButtonState(GUIButtonState.PARADO)
            self.end()
            raise
    
    def startCalibrar(self, tk: Tk, GUIData: GUIData):
        self.GUIData = GUIData
        self.scheduler = tk.after(self.INTERVALO_DE_CHECAGEM, self.processCalibrar)
        self.tk = tk
        self.maiorAccel = 0
        try:
            self.eletronicModule.setup(self.GUIData.COMText.get())
            self.GUIData.setCalibrarState(GUIButtonState.INICIADO)
        except SerialException:
            self.GUIData.setButtonState(GUIButtonState.PARADO)
            self.endCalibrar()
            raise
    
    def endCalibrar(self):
        self.tk.after_cancel(self.scheduler)
        self.eletronicModule.teardown()
        self.GUIData.accel.set(self.maiorAccel)
        self.maiorAccel = 0
        print("Teste")

    def processCalibrar(self):
        data = self.eletronicModule.getData()
        if (data != None):
            self.maiorAccel = max(self.maiorAccel, data["acelerometro"])
        self.scheduler = self.tk.after(self.INTERVALO_DE_CHECAGEM, self.processCalibrar)

    def end(self):
        self.tk.after_cancel(self.scheduler)
        self.eletronicModule.teardown()
        self.midiService.teardown()

    def process(self):
        '''@private'''
        eletronicData = self.eletronicModule.getData()
        if(eletronicData != None):
            self.processToque(eletronicData)
            self.processAccel(eletronicData)
        # pode aumentar o intervalo para testar com o Mock
        self.scheduler = self.tk.after(self.INTERVALO_DE_CHECAGEM, self.process) # chama a si mesmo depois de um determinado período de tempo
    
    def processToque(self, eletronicData):
        '''@private'''
        TOQUE_NOTE_DURATION = 200 # em milisegundos
        CANAL = 0
        nota = self.selecionaNota(self.GUIData, eletronicData)
        if(eletronicData["toque"] >= 30):
            self.ultimaNota = ""
        if(nota is not None) and (eletronicData["toque"] < 30) and self.ultimaNota != nota:
            self.ultimaNota = nota
            self.send(CANAL, nota, self.TOUCH_NOTE_VELOCITY)
            self.tk.after(TOQUE_NOTE_DURATION, lambda: self.send(CANAL, nota, self.TOUCH_NOTE_VELOCITY, False))
    
    def selecionaNota(self, GUIData: GUIData, eletronicData):
        '''@private'''
        preset = GUIData.getNotePreset()
        giro = eletronicData["giroscopio"]
        if (giro <= preset["angulo_inicial"]):
            return None
        for nota in preset["notas"]:
            if giro <= nota["proximo_angulo"]:
                return nota["id"]
        return None

    def processAccel(self, eletronicData):
        '''@private'''
        ACCEL_PRESET = self.GUIData.getAccelPreset()
        CANAL = ACCEL_PRESET["canal"]
        NOTA = ACCEL_PRESET["nota"]
        ACCEL_NOTE_VELOCITY = 120
        ACCEL_NOTE_DURATION = 200 # em milisegundos
        if(eletronicData["acelerometro"] >= self.GUIData.getAccel()) and self.permite_accel:
            self.send(CANAL, NOTA, ACCEL_NOTE_VELOCITY)
            print(f"GUI: {self.GUIData.getAccel()}\nDisp: {eletronicData['acelerometro']}")
            self.tk.after(ACCEL_NOTE_DURATION, lambda: self.send(CANAL, NOTA, ACCEL_NOTE_VELOCITY, False))
            self.permite_accel = False

            def setPermiteAccelTrue(self: GUIController):
                self.permite_accel = True
            self.tk.after(1000, lambda: setPermiteAccelTrue(self))
    
    def converteNota(self, nota) -> int:
        '''@private'''
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


