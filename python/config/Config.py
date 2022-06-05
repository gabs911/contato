import json
from config.App import App
from modulos.EletronicModule import EletronicModule
from modulos.MockEletronicModule import MockEletronicModule


environmentEletronic = {
    "teste" : lambda prop: MockEletronicModule(),
    "producao": lambda prop: EletronicModule(prop["porta"])
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
        mode = self.properties["mode"]
        return App(mode, environmentEletronic[mode](self.properties))