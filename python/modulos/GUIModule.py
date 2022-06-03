from modulos.EletronicModule import BaseEletronicModule
from modulos.GUI.GUIController import GUIController
from modulos.GUI.GUIView import GUIView


class GUIModule:
    def __init__(self, eletronicModule: BaseEletronicModule) -> None:
        self.eletronicModule = eletronicModule

    def run(self):
        controller = GUIController(self.eletronicModule)
        GUIView(controller).show()