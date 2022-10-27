from msilib.schema import Component
from tkinter.ttk import Frame

from modulos.GUI.Components.PresetComponent import PresetComponent


class PresetListComponent:
    PRESET_BACKGROUND_FRAME = 'Preset.Background.TFrame'

    def __init__(self, root, presetList: list, dataSetter, component) -> None:
        self.root = root
        self.presetList = presetList
        self.dataSetter = dataSetter
        self.frameToPreset = { }
        self.component = component
        self.selected = ''

    def show(self):
        frame = Frame(self.root, padding=[5], style=self.PRESET_BACKGROUND_FRAME)
        frame.grid(row=2, column=0)
        for item in self.presetList:
            self.factory(item, frame)
    
    def factory(self, item, root):
        presetComponent: PresetComponent = self.component(root, self.frameToPreset, self.dataSetter, item, self)
        presetComponent.show()