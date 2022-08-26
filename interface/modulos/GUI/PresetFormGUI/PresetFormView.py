from modulos.GUI.PresetFormGUI.PresetFormData import PresetFormData
from modulos.GUI.PresetFormGUI.PresetFormController import PresetFormController
from util.TypeCheck import isInt
from util.Event import SimpleEvent
from tkinter import LEFT, RIGHT, StringVar, Tk, Toplevel
from tkinter.ttk import Button, Combobox, Entry, Frame, Label, Spinbox

def valida_angulo(valor):
    if not isInt(valor):
        return False
    valor = int(valor)
    return valor > -359 and valor <= 360

class PresetFormView:
    def __init__(self, tk: Tk, event: SimpleEvent, controller: PresetFormController, data: PresetFormData) -> None:
        self.tk = tk
        self.event = event
        self.controller = controller
        self.data = data

    def show(self) -> None:
        self.root = Toplevel(self.tk)
        self.root.geometry("600x200")
        self.root.focus_set()
        self.data.root = self.root
        self.data.converteParaView()
        # Nome
        self.nomeLabel = Label(self.root, text="Nome")
        self.nomeLabel.grid(row=0, column=0, sticky='W')
        self.nomeEntry = Entry(self.root, textvariable=self.data.nome)
        self.nomeEntry.grid(row=0, column=1)
        
        # Notas
        noteFrame = Frame(self.root, padding=[20])
        noteFrame.grid(row=1, column=0, columnspan=12)

        self.generateNotesFrame(noteFrame)
        
        # Salvar
        self.buttonSave = Button(self.root, text="Salvar", command=self.save)
        self.buttonSave.grid(row=2, column=0)

    def generateNotesFrame(self, root: Frame) -> None:
        # Ângulos
        self.angulosLabel = Label(root, text="Ângulos")
        self.angulosLabel.pack(anchor='nw', expand=True)        

        ## Ângulo Inicial
        self.anguloInicialEntry = Spinbox(root,
            from_= -359, to=360,
            wrap=True, textvariable=self.data.angulo_inicial,
            validate='all', validatecommand=(self.tk.register(valida_angulo), '%P'),
            width=5
            )
        self.anguloInicialEntry.pack(anchor='sw',side=LEFT)

        ## Adição de novas notas
        addNoteButton = Button(root, text="+", command=lambda:self.addNoteBoundary(root))
        addNoteButton.pack(side=RIGHT, anchor='ne')
        
    
    def addNoteBoundary(self, root: Frame):
        frame = Frame(root)
        frame.pack(side=LEFT, anchor='w')

        id = StringVar(frame, "")
        combobox = Combobox(frame, textvariable=id, values=self.controller.getNotasPossiveis(), width=2)
        combobox.grid(row=0, column=0)

        angulo = StringVar(frame, "0")
        spinbox = Spinbox(frame,
            from_= -359, to=360,
            wrap=True, textvariable=angulo,
            validate='all', validatecommand=(self.tk.register(valida_angulo), '%P'),
            width=5
            )
        spinbox.grid(row=1, column=1)
        
        self.data.addNota(angulo, id)

    def save(self):
        self.event.invoke(self.data.converteParaSalvar())
        self.root.destroy()
        

