from modulos.EletronicModule import BaseEletronicModule


class GUIModule:
    def __init__(self, eletronicModule: BaseEletronicModule) -> None:
        self.eletronicModule = eletronicModule

    def run(self):
        print("Gui module successfully created")