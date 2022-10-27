from tkinter import LEFT
from tkinter.ttk import Frame, Widget
from modulos.GUI.GUIData import GUIData


class PresetComponent:
    DEFAULT_FRAME = ''

    def __init__(self, root, frameToPreset, dataSetter, item, presetList) -> None:
        self.root = root
        self.FrameToPreset = frameToPreset
        self.dataSetter = dataSetter
        self.item = item
        self.presetList = presetList

    def show(self):
        self.frame = Frame(self.root, padding=[5], style=self.DEFAULT_FRAME)
        self.frame.pack(fill='x')

        #frame para o preset
        self.presetFrame = Frame(self.frame, style=self.DEFAULT_FRAME)
        self.presetFrame.bind('<Button-1>', (lambda e: self.mouseFunc(e.widget)))
        self.presetFrame.pack(fill='x', expand=True, anchor='w', side=LEFT)

        self.construct()

        self.FrameToPreset[self.presetFrame] = self.item

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