import json
from config.App import App
from os import getenv
from modulos.EletronicModule import EletronicModule
from modulos.MockEletronicModule import MockEletronicModule
from modulos.MidiService import MidiService, MockMidiService
from modulos.FileService import FileService



class Config:
    '''
    Essa classe é responsável de montar o app de formas diferentes baseadas
    no arquivo de configurações, passando os parâmetros necessários para o App
    '''

    TESTE_STRING = "teste"
    PRODUCAO_STRING = "producao"
    DEV_STRING = "dev"

    EletronicModuleMap = {
        TESTE_STRING : lambda prop: MockEletronicModule(),
        PRODUCAO_STRING: lambda prop: EletronicModule()
    }

    MidiServiceMap = {
        TESTE_STRING: lambda prop: MockMidiService(),
        PRODUCAO_STRING: lambda prop: MidiService()
    }

    FileServiceMap = {
        PRODUCAO_STRING: lambda prop: FileService(appDataLocation=getenv('LOCALAPPDATA').replace("\\", "/") + "/" + prop["app_name"] +"/"),
        DEV_STRING: lambda prop: FileService()
    }

    def __init__(self, path):
        with open(path) as jsonFile:
            self.properties = json.load(jsonFile)

    def createApp(self) -> App:
        eletronicEnv = self.properties["ambiente_eletronico"]
        midiEnv = self.properties["ambiente_midi"]
        fileEnv = self.properties["ambiente_file_service"]
        return App(eletronicEnv, midiEnv, fileEnv,
            self.EletronicModuleMap[eletronicEnv](self.properties),
            self.MidiServiceMap[midiEnv](self.properties),
            self.FileServiceMap[fileEnv](self.properties)
        )