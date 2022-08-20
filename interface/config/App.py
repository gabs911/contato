
#Essa é a classe do app 
from modulos.EletronicModule import BaseEletronicModule
from modulos.GUIModule import GUIModule
from modulos.MidiService import MidiService


class App:
    def __init__(self, eletronicEnv: str, midiEnv: str, eletronicModule: BaseEletronicModule, midiService: MidiService):
        self.eletronicEnv = eletronicEnv
        self.midiEnv = midiEnv
        self.eletronicModule = eletronicModule
        self.midiService = midiService

    #o método run vai definir o algoritmo do 
    def run(self):
        print("Seu ambiente para o dispositivo eletronico é: " + self.eletronicEnv)
        print("Seu ambiente para MIDI é: " + self.midiEnv)
        gui = GUIModule(self.eletronicModule, self.midiService)
        gui.run()

