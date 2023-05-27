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

    # Mapeia o Service de arquivos a um ambiente especifíco
    FileServiceMap = {
        #Cria o service de arquivos apontando para a pasta LOCALAPPDATA como a raiz dos paths dos arquivos (específico ao windows)
        PRODUCAO_STRING: lambda prop: FileService(appDataLocation=getenv('LOCALAPPDATA').replace("\\", "/") + "/" + prop["app_name"] +"/"),
        #Cria o service com a pasta em que o programa está sendo rodado como raiz dos paths dos arquivos
        DEV_STRING: lambda prop: FileService()
    }

    def __init__(self, path):
        with open(path) as jsonFile:
            self.properties = json.load(jsonFile)

    def createApp(self) -> App:
        eletronicEnv = self.properties["ambiente_eletronico"]
        midiEnv = self.properties["ambiente_midi"]
        fileEnv = self.properties["ambiente_file_service"]

        print("Seu ambiente para o dispositivo eletronico é: " + eletronicEnv)
        print("Seu ambiente para MIDI é: " + midiEnv)
        print("Seu ambiente de arquivos é: " + fileEnv)

        return App(self.EletronicModuleMap[eletronicEnv](),
            self.MidiServiceMap[midiEnv](),
            self.FileServiceMap[fileEnv](self.properties)
        )