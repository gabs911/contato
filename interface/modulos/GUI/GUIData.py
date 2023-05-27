from enum import Enum, auto
from tkinter import StringVar

class GUIButtonState (Enum):
    STARTING = auto()
    RUNNING = auto()
    STOPED = auto()

class GUIData:
    accel: StringVar = None
    accelPreset = None
    notePreset = None
    buttonText: StringVar = None
    button = None
    calibrarButtonText: StringVar = None
    calibrarButton = None
    COMText: StringVar = None
    MIDIText: StringVar = None
    playButtonState: GUIButtonState = GUIButtonState.STOPED
    calibrationButtonState: GUIButtonState = GUIButtonState.STOPED
    
    def __init__(self) -> None:
        pass
    
    def getAccel(self) -> float:
        return float(self.accel.get())

    def getAccelPreset(self):
        if(self.accelPreset == None):
            print("Nenhum preset de acelerômetro selecionado")
        return self.accelPreset

    def getNotePreset(self):
        if(self.notePreset == None):
            print("Nenhum preset de nota selecionado")
        return self.notePreset
    
    def getPlayButtonState(self) -> GUIButtonState:
        return self.playButtonState
    
    def setPlayButtonState(self, state: GUIButtonState):
        '''Seta o estado do botão de tocar e altera o texto dele para indicar o novo estado'''
        self.playButtonState = state
        match state:
            case GUIButtonState.STARTING:
                self.buttonText.set("Iniciando")
                self.button.state(["disabled"])
            case GUIButtonState.RUNNING:
                self.buttonText.set("Parar")
                self.button.state(["!disabled"])
            case GUIButtonState.STOPED:
                self.buttonText.set("Tocar")
                self.button.state(["!disabled"])

    def getCalibrationButtonState(self) -> GUIButtonState:
        return self.calibrationButtonState
    
    def setCalibrationButtonState(self, state: GUIButtonState):
        '''Seta o estado do botão de calibrar e altera o texto dele para indicar o novo estado'''
        self.calibrationButtonState = state
        match state:
            case GUIButtonState.STARTING:
                self.calibrarButtonText.set("Iniciando")
                self.calibrarButton.state(["disabled"])
            case GUIButtonState.RUNNING:
                self.calibrarButtonText.set("Parar")
                self.calibrarButton.state(["!disabled"])
            case GUIButtonState.STOPED:
                self.calibrarButtonText.set("Calibrar")
                self.calibrarButton.state(["!disabled"])
    
    def setAccelPreset(self, accelPreset):
        self.accelPreset = accelPreset
    
    def setNotePreset(self, notePreset):
        self.notePreset = notePreset



