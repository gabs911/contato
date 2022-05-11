
#Essa é a classe do app 
from modulos.EletronicModule import BaseEletronicModule
from modulos.GUIModule import GUIModule


class App:
    def __init__(self, message, eletronicModule: BaseEletronicModule):
        self.message = message
        self.eletronicModule = eletronicModule

    #o método run vai definir o algoritmo do 
    def run(self):
        print("Seu ambiente é: " + self.message)
        self.eletronicModule.setup()
        gui = GUIModule(self.eletronicModule)
        gui.run()

