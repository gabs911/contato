from tkinter import LEFT, RIGHT
from tkinter.ttk import Frame, Label
from modulos.GUI.Components.PresetComponent import PresetComponent
from modulos.GUI.Forms.AccelFormGUI.AccelFormData import AccelFormData
from modulos.GUI.Forms.AccelFormGUI.AccelFormModule import AccelFormModule
from modulos.GUI.Forms.FormData import FormData
from modulos.GUI.Forms.FormModule import FormModule
from modulos.GUI.GUIData import GUIData
from modulos.FileService import FileService

class AccelPresetComponent (PresetComponent):
    def __init__(self,root, fileService: FileService, frameToPreset, dataReference: GUIData, item, presetList) -> None:
        super().__init__(root,fileService , frameToPreset, dataReference, item, presetList)
    
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
    
    def getPresetModule(self) -> FormModule:
        return AccelFormModule(self.fileService)
    
    def getFormData(self, item) -> FormData:
        super().getFormData(item)
        return AccelFormData(item)
        