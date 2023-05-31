from math import floor
from serial import SerialException
from tkinter import Tk
from modulos.GUI.GUIData import GUIButtonState
from modulos.EletronicModule import BaseEletronicModule
from modulos.FileService import FileService
from modulos.MidiService import MidiService
from modulos.GUI.GUIData import GUIData


class GUIController:
    CHECKING_INTERVAL = 1
    TOUCH_NOTE_VELOCITY = 100

    def __init__(self, eletronicModule: BaseEletronicModule, midiService: MidiService, fileService: FileService) -> None:
        self.eletronicModule = eletronicModule
        self.midiService = midiService
        self.fileService = fileService
        self.scheduler = ""
        self.allow_accel = True
        self.ultimaNota = ""
  
    def getAccelPresets(self) -> list:
        return self.fileService.getAccelPresets()

    def getNotePresets(self) -> list:
        return self.fileService.getNotePresets()

    def saveNotesPreset(self, item, nome: str) -> None:
        self.fileService.saveNotesPreset(item, nome)

    def listCOMPorts(self):
        return self.eletronicModule.listCOMPorts()

    def listMIDIPorts(self):
        return self.midiService.listMIDIPorts()
    
    def startCalibration(self, tk: Tk, GUIData: GUIData):
        '''Inicializa processo de calibração '''
        self.GUIData = GUIData
        self.scheduler = tk.after(self.CHECKING_INTERVAL, self.processCalibration)
        self.tk = tk
        self.maiorAccel = 0
        try:
            self.eletronicModule.setup(self.GUIData.COMText.get())
            self.GUIData.setCalibrationButtonState(GUIButtonState.RUNNING)
        except SerialException:
            self.GUIData.setPlayButtonState(GUIButtonState.STOPED)
            self.endCalibration()
            raise
    
    def endCalibration(self):
        '''Termina processo de calibração e seta o novo valor do acelerômetro'''
        self.tk.after_cancel(self.scheduler)
        self.eletronicModule.teardown()
        self.GUIData.accel.set(floor(self.maiorAccel))
        self.maiorAccel = 0
        print("Teste")

    def processCalibration(self):
        '''Função de uso interno da classe para processar a entrada de dados atual e agendar o novo processamento'''
        data = self.eletronicModule.getData()
        if (data != None):
            self.maiorAccel = max(self.maiorAccel, data["acelerometro"])
        self.scheduler = self.tk.after(self.CHECKING_INTERVAL, self.processCalibration)

    def start(self, tk: Tk, GUIData: GUIData):
        '''Faz o setup para tocar as notas e inicializa processamento dos dados do Contato'''
        self.GUIData = GUIData
        self.scheduler = tk.after(self.CHECKING_INTERVAL, self.process)
        self.tk = tk
        try:
            self.midiService.setup(int(self.GUIData.MIDIText.get().split(" ")[-1]))
            self.eletronicModule.setup(self.GUIData.COMText.get())
            self.GUIData.setPlayButtonState(GUIButtonState.RUNNING)
            print("Start")
        except SerialException:
            # Caso ocorra qualquer erro na hora de inicializar, reseta o botão e termina o processo
            self.GUIData.setPlayButtonState(GUIButtonState.STOPED)
            self.end()
            raise

    def end(self):
        '''Termina processamento dos dados do Contato'''
        self.tk.after_cancel(self.scheduler)
        self.eletronicModule.teardown()
        self.midiService.teardown()

    def process(self):
        '''Função de uso interno da classe para processar a entrada de dados atual e agendar o novo processamento'''
        eletronicData = self.eletronicModule.getData()
        if(eletronicData != None):
            self.processTouch(eletronicData)
            self.processAccel(eletronicData)
        # chama a si mesmo depois de um determinado período de tempo
        self.scheduler = self.tk.after(self.CHECKING_INTERVAL, self.process)
    
    def processTouch(self, eletronicData):
        '''Processa a informação de toque e giroscópio'''
        TOQUE_NOTE_DURATION = 200 # em milisegundos
        CANAL = 0
        nota = self.selectNote(self.GUIData, eletronicData)
        if(eletronicData["toque"] == 0):
            self.ultimaNota = ""
        if(nota is not None) and (eletronicData["toque"] == 1) and self.ultimaNota != nota:
            self.ultimaNota = nota
            self.send(CANAL, nota, self.TOUCH_NOTE_VELOCITY)
            self.tk.after(TOQUE_NOTE_DURATION, lambda: self.send(CANAL, nota, self.TOUCH_NOTE_VELOCITY, False))
    
    def selectNote(self, GUIData: GUIData, eletronicData):
        '''Seleciona qual a nota deve ser tocada de acordo com o ângulo passado'''
        preset = GUIData.getNotePreset()
        giro = eletronicData["giroscopio"]
        if (giro <= preset["angulo_inicial"]):
            return None
        for nota in preset["notas"]:
            if giro <= nota["proximo_angulo"]:
                return nota["id"]
        return None

    def processAccel(self, eletronicData):
        '''Processa informações do acelerômetro'''
        ACCEL_PRESET = self.GUIData.getAccelPreset()
        CHANNEL = ACCEL_PRESET["canal"]
        NOTE = ACCEL_PRESET["nota"]
        ACCEL_NOTE_VELOCITY = 120
        ACCEL_NOTE_DURATION = 200 # em milisegundos
        if(eletronicData["acelerometro"] >= self.GUIData.getAccel()) and self.allow_accel:
            self.send(CHANNEL, NOTE, ACCEL_NOTE_VELOCITY)
            print(f"GUI: {self.GUIData.getAccel()}\nDisp: {eletronicData['acelerometro']}")
            self.tk.after(ACCEL_NOTE_DURATION, lambda: self.send(CHANNEL, NOTE, ACCEL_NOTE_VELOCITY, False))
            self.allow_accel = False
            self.tk.after(ACCEL_NOTE_DURATION, lambda: self.setPermiteAccelTrue(self))
    
    def setPermiteAccelTrue(self):
        '''
        Torna a variável que permite tocar o acelerômetro para true
        Por algum motivo o python exige que eu transforme em função para poder passar para o lambda e funcionar
        '''
        self.allow_accel = True
    
    def convertNote(self, nota) -> int:
        '''Converte a nota do string para o id MIDI da nota, baseado no arquivo de mapeamento'''
        if(type(nota) is str):
            return self.fileService.getNoteConverter()[nota]
        return nota

    def send(self, canal: int, nota, velocity: int, on = True):
        '''
        Envia a informação para o Midiout
        :canal: canal em que será enviada a nota
        :nota: nota a ser tocada
        :velocity: velocidade da nota
        :on: Se é para iniciar ou parar uma nota: True - > liga, False -> desliga
        '''
        self.midiService.send(canal, on, self.convertNote(nota), velocity)


