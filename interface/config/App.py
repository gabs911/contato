
#Essa é a classe do app 
from logging import getLogger, info
from modulos.EletronicModule import BaseEletronicModule
from modulos.GUIModule import GUIModule
from modulos.MidiService import MidiService
from modulos.FileService import FileService
from util.logFunction import logException



class App:
    def __init__(self,eletronicModule: BaseEletronicModule, midiService: MidiService, fileService: FileService):
        self.eletronicModule = eletronicModule
        self.midiService = midiService
        self.fileService = fileService

    @logException
    def run(self):
        '''
        Cria o módulo de interface usando as dependêcias passadas pelo Config 
        '''
        logger = getLogger('root')
        logger.info('Application Started')
        gui = GUIModule(self.eletronicModule, self.midiService, self.fileService)
        gui.run()

