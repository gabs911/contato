from tkinter import LEFT, RIGHT
from tkinter.ttk import Label
from modulos.GUI.Components.PresetComponent import PresetComponent
from modulos.GUI.GUIData import GUIData

class AccelPresetComponent (PresetComponent):
    def __init__(self,root, frameToPreset, dataReference: GUIData, item, presetList) -> None:
        super().__init__(root, frameToPreset, dataReference, item, presetList)
    
    def construct(self):
        #nome do preset
        label_nome = Label(self.presetFrame, text=self.item['nome'])
        label_nome.bind('<Button-1>', (lambda e: self.mouseFunc(e.widget.master)))
        # label_nome.grid(row=0, column=0, sticky='W')
        label_nome.pack(anchor='nw', side=LEFT)

        label_valor = Label(self.presetFrame, text=self.item["nota"], justify='right', padding=[0,20,0,0])
        label_valor.bind('<Button-1>', (lambda e: self.mouseFunc(e.widget.master)))
        # label_valor.grid(row=1, column=1, sticky='E')
        label_valor.pack(anchor='se', side=RIGHT)
        