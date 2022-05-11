import json
from config.App import App
from modulos.EletronicModule import EletronicModule
from modulos.MockEletronicModule import MockEletronicModule

#Essa classe é responsável de montar o app de formas diferentes baseadas
#no arquivo de configurações, passando os parâmetros necessários

environmentEletronic = {
    "teste" : lambda: MockEletronicModule(1,1),
    "homologacao": lambda: EletronicModule()
}

class Config:
    def __init__(self, path):
        with open(path) as jsonFile:
            self.properties = json.load(jsonFile)

    def createApp(self):
        mode = self.properties["mode"]
        return App(mode, environmentEletronic[mode]())