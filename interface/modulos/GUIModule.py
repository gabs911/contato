from modulos.GUI.Forms.PresetFormGUI.PresetFormModule import PresetFormModule
from modulos.EletronicModule import BaseEletronicModule
from modulos.GUI.GUIController import GUIController
from modulos.GUI.GUIView import GUIView
from modulos.MidiService import MidiService
from modulos.FileService import FileService


class GUIModule:
    def __init__(self, eletronicModule: BaseEletronicModule, midiService: MidiService, fileService: FileService) -> None:
        self.eletronicModule = eletronicModule
        self.midiService = midiService
        self.fileService = fileService

    def run(self):
        controller = GUIController(self.eletronicModule, self.midiService, self.fileService)
        GUIView(controller, PresetFormModule(self.fileService)).show()