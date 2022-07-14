from modulos.EletronicModule import BaseEletronicModule
from modulos.GUI.GUIController import GUIController
from modulos.GUI.GUIView import GUIView
from modulos.MidiService import MidiService


class GUIModule:
    def __init__(self, eletronicModule: BaseEletronicModule, midiService: MidiService) -> None:
        self.eletronicModule = eletronicModule
        self.midiService = midiService

    def run(self):
        controller = GUIController(self.eletronicModule, self.midiService)
        GUIView(controller).show()