from tkinter import LEFT, RIGHT, PhotoImage, messagebox
from tkinter.ttk import Button, Frame, Widget
from modulos.GUI.Forms.FormData import FormData
from modulos.GUI.Forms.FormModule import FormModule
from modulos.GUI.GUIData import GUIData
from modulos.FileService import FileService
from util.Event import SimpleEvent


class PresetComponent:
    DEFAULT_FRAME = 'TFrame'

    def __init__(self, root, fileService: FileService, frameToPreset: dict, dataSetter, item, presetList) -> None:
        self.fileService = fileService
        self.root = root
        self.FrameToPreset = frameToPreset
        self.dataSetter = dataSetter
        self.item = item
        self.presetList = presetList
        self.deleteImage = PhotoImage(file="resources/imagens/trash.png")

    def show(self):
        self.frame = Frame(self.root, padding=[5], style=self.DEFAULT_FRAME)
        self.frame.pack(fill='x')

        #frame para o preset
        self.presetFrame = Frame(self.frame, style=self.DEFAULT_FRAME)
        self.presetFrame.bind('<Button-1>', (lambda e: self.mouseFunc(e.widget)))
        self.presetFrame.pack(fill='x', expand=True, anchor='w', side=LEFT)

        self.construct()

        self.FrameToPreset[self.presetFrame] = self.item
        self.generateButtons(self.frame, self.presetFrame,  self.root)

    def construct(self):
        pass

    def select(self, widget: Widget):
        widget.state(['selected'])
        for child in widget.children.values():
            self.select(child)

    def unselect(self, widget: Widget):
        widget.state(['!selected'])
        for child in widget.children.values():
            self.unselect(child)

    def mouseFunc(self, widget: Widget):
        if (type(self.presetList.selected) == Frame):
            self.unselect(self.presetList.selected)
        self.dataSetter(self.FrameToPreset[widget])
        self.presetList.selected = widget
        self.select(widget)
    
    def generateButtons(self, frame, noteFrame, root) -> None:
        buttonFrame = Frame(frame, style=self.DEFAULT_FRAME)
        buttonFrame.pack(anchor='e', side=RIGHT)
        
        #adiciona botão de editar
        edit_button = Button(buttonFrame, text="Editar", command=lambda: self.generateEditButton(root, noteFrame), width=6)
        edit_button.grid(row=0, column=0)

        #adiciona botão de deletar
        delete_button = Button(buttonFrame, image=self.deleteImage, command=lambda: self.generateDelete(noteFrame))
        delete_button.grid(row=0, column=1)
    
    def generateEditButton(self, root: Frame, presetFrame: Frame):
        item = self.item
        data = self.getFormData(item)
        formModule = self.getPresetModule()
        event = SimpleEvent()
        event.add_listenter(lambda _: self.deletePreset(item, presetFrame))
        event.add_listenter(lambda preset: self.presetList.factory(preset, root))
        event.add_listenter(lambda preset: formModule.getController().savePreset(preset, preset["nome"]))
        self.presetList.generateForm(root, event, data)
    
    def getFormData(self, item) -> FormData:
        pass    
    
    def generateDelete(self, presetFrame: Frame):
        item = self.FrameToPreset[presetFrame]
        confirmacao = messagebox.askokcancel(
            title="Confimação de deleção",
            message=f"Tem certeza que deseja deletar o preset \"{item['nome']}\"?",
            icon=messagebox.WARNING
            )
        if confirmacao:
            self.deletePreset(item, presetFrame)

    def deletePreset(self, item, presetFrame: Frame):
        print(item)
        self.FrameToPreset.pop(presetFrame)
        controller = self.getPresetModule().getController()
        controller.deletePreset(item["nome"])
        presetFrame.master.pack_forget()
        presetFrame.master.destroy()

    def getPresetModule(self) -> FormModule:
        pass