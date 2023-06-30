import json
from config.App import App
from os import getenv
from time import strftime
import logging
from modulos.EletronicModule import EletronicModule
from modulos.MockEletronicModule import MockEletronicModule
from modulos.MidiService import MidiService, MockMidiService
from modulos.FileService import FileService



class Config:
    '''
    Essa classe é responsável de montar o app de formas diferentes baseadas
    no arquivo de configurações, passando os parâmetros necessários para a classe App
    '''

    TESTE_STRING = "teste"
    PRODUCAO_STRING = "producao"
    DEV_STRING = "dev"

    # Mapeia o módulo eletrônico a um ambiente especifíco 
    EletronicModuleMap = {
        TESTE_STRING : lambda :MockEletronicModule(),
        PRODUCAO_STRING: lambda : EletronicModule()
    }

    # Mapeia o Service de MIDI a um ambiente especifíco 
    MidiServiceMap = {
        TESTE_STRING: lambda : MockMidiService(),
        PRODUCAO_STRING: lambda : MidiService()
    }

    # Mapeia a pasta base dos arquivos baseado no ambiente de arquivos
    FileBaseMap = {
        PRODUCAO_STRING: lambda prop: getenv('LOCALAPPDATA').replace("\\", "/") + "/" + prop["app_name"] +"/",
        DEV_STRING: lambda prop: ""
    }

    def __init__(self, path):
        with open(path) as jsonFile:
            self.properties = json.load(jsonFile)

    def createApp(self) -> App:
        eletronicEnv = self.properties["ambiente_eletronico"]
        midiEnv = self.properties["ambiente_midi"]
        fileEnv = self.properties["ambiente_file_service"]

        fileBaseFolder = self.FileBaseMap[fileEnv](self.properties)

        self.setupLogging(fileBaseFolder)

        self.logger.info("Seu ambiente para o dispositivo eletronico é: " + eletronicEnv)
        self.logger.info("Seu ambiente para MIDI é: " + midiEnv)
        self.logger.info("Seu ambiente de arquivos é: " + fileEnv)

        return App(self.EletronicModuleMap[eletronicEnv](),
            self.MidiServiceMap[midiEnv](),
            FileService(fileBaseFolder)
        )
    
    def setupLogging(self, baseFolder) -> None:
        numeric_level = getattr(logging, str(self.properties["log_level"]).upper(), logging.DEBUG)
        # create logger
        self.logger = logging.getLogger('root')
        self.logger.setLevel(numeric_level)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        file_handler = logging.FileHandler(filename=f"{baseFolder}logs/{strftime('%m-%d-%Y-%I-%M-%S')}.log", mode="w+", encoding="UTF-8")
        file_handler.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)
        self.logger.addHandler(file_handler)