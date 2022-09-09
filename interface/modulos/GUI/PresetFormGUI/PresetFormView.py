from modulos.GUI.PresetFormGUI.PresetFormData import PresetFormData
from modulos.GUI.PresetFormGUI.PresetFormController import PresetFormController
from util.TypeCheck import isInt
from util.Event import SimpleEvent
from tkinter import LEFT, RIGHT, TOP, StringVar, Tk, Toplevel
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
        self.noteFrames = []

    def show(self) -> None:
        self.root = Toplevel(self.tk)
        self.root.geometry("600x200")
        self.root.focus_set()
        self.data.root = self.root
        self.data.converteParaView()
        if self.data.nome.get() == "":
            self.root.title("Novo Preset de notas")
        else:
            self.root.title(f"Editar Preset {self.data.nome.get()}")
        
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
            validate='focusout', validatecommand=(self.tk.register(valida_angulo), '%P'),
            width=5
            )
        self.anguloInicialEntry.pack(anchor='sw',side=LEFT)

        ## Popula notas
        for nota in self.data.notas:
            self.generateNote(root, nota)

        buttonFrame = Frame(root, padding=[0,10,0,0])
        buttonFrame.pack(side=RIGHT, anchor='e')

        ## Adição de novas notas
        addNoteButton = Button(buttonFrame, text="+", command=lambda:self.generateNewNote(root))
        addNoteButton.pack(side=TOP, anchor='e', expand=1)    

        ## Remoção de notas
        deleteNoteButton = Button(buttonFrame, text='-', command=self.deleteNote)
        deleteNoteButton.pack(side=TOP, anchor='e', expand=1)
        
    def generateNewNote(self, root: Frame):
        nota = self.data.notaNula()
        self.generateNote(root, nota)
        self.data.addNota(nota["angulo"], nota["id"])
    
    def generateNote(self, root: Frame, nota):
        '''
        param 3 nota: nota no formato {"id", "angulo"}
        '''
        frame = Frame(root, padding=[0,20, 0, 0])
        frame.pack(side=LEFT, anchor='w')
        self.noteFrames.append(frame)

        combobox = Combobox(frame, textvariable=nota["id"],
            width=2,
            values=self.controller.getNotasPossiveis(), validate='all',
            validatecommand=(self.tk.register(lambda v: v in self.controller.getNotasPossiveis() + [""]), '%P'))
        combobox.grid(row=0, column=0)

        spinbox = Spinbox(frame,
            from_= -359, to=360,
            wrap=True, textvariable=nota["angulo"],
            validate='all', validatecommand=(self.tk.register(valida_angulo), '%P'),
            width=5
            )
        spinbox.grid(row=1, column=1)

    def deleteNote(self):
        self.data.deletaNota()
        frame:Frame = self.noteFrames.pop()
        frame.destroy()
        
    def save(self):
        self.event.invoke(self.data.converteParaSalvar())
        self.root.destroy()
        

