import json
from config.App import App
from modulos.EletronicModule import EletronicModule
from modulos.MockEletronicModule import MockEletronicModule
from modulos.MidiService import MidiService, MockMidiService

TESTE_STRING = "teste"
PRODUCAO_STRING = "producao"

EletronicModuleMap = {
    TESTE_STRING : lambda prop: MockEletronicModule(),
    PRODUCAO_STRING: lambda prop: EletronicModule(prop["serial_port"])
}

MidiServiceMap = {
    TESTE_STRING: lambda prop: MockMidiService(),
    PRODUCAO_STRING: lambda prop: MidiService(prop["midi_port"])
}

class Config:
    '''
    Essa classe é responsável de montar o app de formas diferentes baseadas
    no arquivo de configurações, passando os parâmetros necessários para o App
    '''
    def __init__(self, path):
        with open(path) as jsonFile:
            self.properties = json.load(jsonFile)

    def createApp(self) -> App:
        eletronicEnv = self.properties["ambiente_eletronico"]
        midiEnv = self.properties["ambiente_midi"]
        return App(eletronicEnv,
            midiEnv,
            EletronicModuleMap[eletronicEnv](self.properties),
            MidiServiceMap[midiEnv](self.properties)
        )