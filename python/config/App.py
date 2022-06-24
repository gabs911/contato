
#Essa é a classe do app 
from modulos.EletronicModule import BaseEletronicModule
from modulos.GUIModule import GUIModule
from modulos.MidiService import MidiService


class App:
    def __init__(self, message, eletronicModule: BaseEletronicModule, midiService: MidiService):
        self.message = message
        self.eletronicModule = eletronicModule
        self.midiService = midiService

    #o método run vai definir o algoritmo do 
    def run(self):
        print("Seu ambiente é: " + self.message)
        self.eletronicModule.setup()
        gui = GUIModule(self.eletronicModule, self.midiService)
        gui.run()

