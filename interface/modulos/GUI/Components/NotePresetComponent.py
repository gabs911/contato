from tkinter.ttk import Label
from modulos.GUI.Components.PresetComponent import PresetComponent
from modulos.GUI.Forms.FormData import FormData
from modulos.GUI.Forms.FormModule import FormModule
from modulos.GUI.Forms.PresetFormGUI.PresetFormData import PresetFormData
from modulos.GUI.Forms.PresetFormGUI.PresetFormModule import PresetFormModule

class NotePresetComponent(PresetComponent):
    def __init__(self, root, frameToPreset: dict, dataSetter, item, presetList) -> None:
        super().__init__(root, frameToPreset, dataSetter, item, presetList)
    
    def construct(self):
        super().construct()
        #nome do preset
        label_nome = Label(self.presetFrame, text=self.item['nome'])
        label_nome.bind('<Button-1>', (lambda e: self.mouseFunc(e.widget.master)))
        label_nome.grid(row=0, column=0, columnspan=12, sticky='W')

        #valor do ângulo de inicio
        label_inicio = Label(self.presetFrame, text=str(self.item['angulo_inicial']))
        label_inicio.grid(row=2, column=0)
        for zipper in zip(self.item['notas'], range(len(self.item['notas']))):
            nota, i = zipper
            #nome da nota
            nota_nome = Label(self.presetFrame, text=nota["id"])
            nota_nome.grid(row=1, column=2*i + 1)
            #valor final do ângulo da nota
            nota_valor_final = Label(self.presetFrame, text=nota['proximo_angulo'])
            nota_valor_final.grid(row=2, column=2*i + 2)
    
    def getFormData(self, item) -> FormData:
        return PresetFormData(item)
    
    def getPresetModule(self) -> FormModule:
        return PresetFormModule()
