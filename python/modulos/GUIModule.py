from modulos.EletronicModule import BaseEletronicModule
from modulos.GUI.GUIController import GUIController


class GUIModule:
    def __init__(self, eletronicModule: BaseEletronicModule) -> None:
        self.eletronicModule = eletronicModule

    def run(self):
        tester = self.eletronicModule.getData()
        GUIController(self.eletronicModule).view().show()