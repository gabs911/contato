from msilib.schema import Component
from tkinter import BOTTOM, Tk
from tkinter.ttk import Button, Frame

from modulos.GUI.Components.PresetComponent import PresetComponent
from modulos.GUI.Forms.PresetFormGUI.PresetFormModule import PresetFormModule
from util.Event import SimpleEvent


class PresetListComponent:
    PRESET_BACKGROUND_FRAME = 'Preset.Background.TFrame'

    def __init__(self, root, parent, presetList: list, dataSetter, component) -> None:
        self.root = root
        self.parent = parent
        self.presetList = presetList
        self.dataSetter = dataSetter
        self.frameToPreset = { }
        self.component = component
        self.selected = ''

    def show(self):
        self.frame = Frame(self.root, padding=[5], style=self.PRESET_BACKGROUND_FRAME)
        self.frame.grid(row=2, column=0)
        for item in self.presetList:
            self.factory(item, self.frame)
        
        event = self.generateAddEvent()
        addButton = Button(self.frame, padding=[5], text="+",
                command=lambda: self.generateForm(self.frame, event))
        addButton.pack(anchor='s', side=BOTTOM)
    
    def factory(self, item, root):
        presetComponent: PresetComponent = self.component(root, self.frameToPreset, self.dataSetter, item, self)
        self.presetForm = presetComponent.getPresetModule()
        presetComponent.show()
    
    def generateAddEvent(self):
        controller = self.presetForm.getController()
        event = SimpleEvent()
        event.add_listenter(lambda preset: controller.savePreset(preset, preset["nome"]))
        event.add_listenter(lambda preset: self.factory(preset, self.frame))
        return event

    def generateForm(self, root: Tk, event: SimpleEvent, data = None):
        formView = self.presetForm.createView(root, event, data)
        formView.show()