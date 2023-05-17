
#Essa é a classe do app 
from modulos.EletronicModule import BaseEletronicModule
from modulos.GUIModule import GUIModule
from modulos.MidiService import MidiService
from modulos.FileService import FileService


class App:
    def __init__(self, eletronicEnv: str, midiEnv: str, fileEnv: str ,eletronicModule: BaseEletronicModule, midiService: MidiService, fileService: FileService):
        self.eletronicEnv = eletronicEnv
        self.midiEnv = midiEnv
        self.fileEnv = fileEnv
        self.eletronicModule = eletronicModule
        self.midiService = midiService
        self.fileService = fileService

    def run(self):
        '''
        Injeta as dependências do módulo de Interface e o cria
        '''
        print("Seu ambiente para o dispositivo eletronico é: " + self.eletronicEnv)
        print("Seu ambiente para MIDI é: " + self.midiEnv)
        print("Seu ambiente de arquivos é: " + self.fileEnv)
        gui = GUIModule(self.eletronicModule, self.midiService, self.fileService)
        gui.run()

