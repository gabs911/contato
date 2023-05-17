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

    # Cria o módulo eletrônico baseado no ambiente
    EletronicModuleMap = {
        TESTE_STRING : lambda :MockEletronicModule(),
        PRODUCAO_STRING: lambda : EletronicModule()
    }

    # Cria o Service de MIDI baseado no ambiente 
    MidiServiceMap = {
        TESTE_STRING: lambda : MockMidiService(),
        PRODUCAO_STRING: lambda : MidiService()
    }

    # Cria o Service de arquivos baseado no ambiente
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
            self.EletronicModuleMap[eletronicEnv](),
            self.MidiServiceMap[midiEnv](),
            self.FileServiceMap[fileEnv](self.properties)
        )