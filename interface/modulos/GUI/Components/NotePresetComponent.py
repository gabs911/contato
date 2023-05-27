from tkinter.ttk import Label
from modulos.GUI.Components.PresetComponent import PresetComponent
from modulos.GUI.Forms.FormData import FormData
from modulos.GUI.Forms.FormModule import FormModule
from modulos.GUI.Forms.PresetFormGUI.PresetFormData import PresetFormData
from modulos.GUI.Forms.PresetFormGUI.PresetFormModule import PresetFormModule
from modulos.FileService import FileService

class NotePresetComponent(PresetComponent):
    def __init__(self, root, fileService: FileService, frameToPreset: dict, dataSetter, item, presetList) -> None:
        super().__init__(root, fileService, frameToPreset, dataSetter, item, presetList)
    
    def construct(self):
        super().construct()
        #nome do preset
        label_name = Label(self.presetFrame, text=self.item['nome'])
        label_name.bind('<Button-1>', (lambda e: self.mouseFunc(e.widget.master)))
        label_name.grid(row=0, column=0, columnspan=12, sticky='W')

        #valor do ângulo de inicio
        start_label = Label(self.presetFrame, text=str(self.item['angulo_inicial']))
        start_label.grid(row=2, column=0)
        for zipper in zip(self.item['notas'], range(len(self.item['notas']))):
            note, i = zipper
            #nome da nota
            note_name = Label(self.presetFrame, text=note["id"])
            note_name.grid(row=1, column=2*i + 1)
            #valor final do ângulo da nota
            next_note_angle = Label(self.presetFrame, text=note['proximo_angulo'])
            next_note_angle.grid(row=2, column=2*i + 2)
    
    def getFormData(self, item) -> FormData:
        return PresetFormData(item)
    
    def getPresetModule(self) -> FormModule:
        return PresetFormModule(self.fileService)
