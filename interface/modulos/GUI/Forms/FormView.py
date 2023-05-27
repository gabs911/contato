
from tkinter import BOTTOM, Tk, Toplevel
from tkinter.ttk import Button
from modulos.GUI.Forms.FormData import FormData
from util.Event import SimpleEvent


class FormView:
    '''Esqueleto para a janela de criação/edição do preset'''
    def __init__(self,tk: Tk, event: SimpleEvent, data: FormData) -> None:
        self.event = event
        self.tk = tk
        self.data = data
    
    def show(self) -> None:
        '''Cria a uma nova janela e converte os dados do Preset para a View'''
        self.root = Toplevel(self.tk)
        self.root.geometry("")
        self.root.focus_set()
        self.data.root = self.root
        self.data.convertForView()
        
        self.construct()

        self.buttonSave = Button(self.root, text="Salvar", command=self.save)
        self.buttonSave.pack(anchor='sw', side=BOTTOM)

    def construct(self) -> None:
        '''Popula a janela com os componentes de GUI'''
        pass

    def save(self):
        '''Passa as informações convertidas para o evento de salvar e fecha a janela'''
        self.event.invoke(self.data.convertToSave())
        self.root.destroy()