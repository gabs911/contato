from enum import Enum, auto
from tkinter import StringVar

class GUIButtonState (Enum):
    INICIANDO = auto()
    INICIADO = auto()
    PARADO = auto()

class GUIData:
    accel = 0
    accelPreset = None
    notePreset = None
    buttonText: StringVar = None
    button = None
    
    def __init__(self) -> None:
        pass
    
    def getAccel(self):
        return self.accel

    def getAccelPreset(self):
        if(self.accelPreset == None):
            print("Nenhum preset de acelerômetro selecionado")
        return self.accelPreset

    def getNotePreset(self):
        if(self.notePreset == None):
            print("Nenhum preset de nota selecionado")
        return self.notePreset
    
    def setButtonState(self, state: GUIButtonState):
        match state:
            case GUIButtonState.INICIANDO:
                self.buttonText.set("Iniciando")
                self.button.state(["disabled"])
            case GUIButtonState.INICIADO:
                self.buttonText.set("Parar")
                self.button.state(["!disabled"])
            case GUIButtonState.PARADO:
                self.buttonText.set("Tocar")
                self.button.state(["!disabled"])



