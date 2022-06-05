from modulos.EletronicModule import BaseEletronicModule
from modulos.GUI.GUIController import GUIController
from modulos.GUI.GUIView import GUIView
from modulos.MidiService import MidiService


class GUIModule:
    def __init__(self, eletronicModule: BaseEletronicModule) -> None:
        self.eletronicModule = eletronicModule

    def run(self):
        midiService = MidiService()
        controller = GUIController(self.eletronicModule, midiService)
        GUIView(controller).show()