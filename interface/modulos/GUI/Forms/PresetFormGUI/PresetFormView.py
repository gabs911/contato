from modulos.GUI.Forms.FormView import FormView
from modulos.GUI.Forms.PresetFormGUI.PresetFormData import PresetFormData
from modulos.GUI.Forms.PresetFormGUI.PresetFormController import PresetFormController
from util.TypeCheck import isInt
from util.Event import SimpleEvent
from tkinter import BOTTOM, LEFT, RIGHT, TOP, StringVar, Tk, Toplevel
from tkinter.ttk import Button, Combobox, Entry, Frame, Label, Spinbox

def validateAngle(value):
    if not isInt(value):
        return False
    value = int(value)
    return value > -359 and value <= 360

class PresetFormView(FormView):
    def __init__(self, tk: Tk, event: SimpleEvent, controller: PresetFormController, data: PresetFormData) -> None:
        super().__init__(tk, event, data)
        self.controller = controller
        self.noteFrames = []
        self.data: PresetFormData        
    
    def construct(self) -> None:
        super().construct()
        #set Titulo
        if self.data.name.get() == "":
            self.root.title("Novo Preset de notas")
        else:
            self.root.title(f"Editar Preset {self.data.name.get()}")
        
        # Nome
        self.frame = Frame(self.root)
        self.frame.pack()
        self.nomeLabel = Label(self.frame, text="Nome")
        self.nomeLabel.grid(row=0, column=0, sticky='W')
        self.nomeEntry = Entry(self.frame, textvariable=self.data.name)
        self.nomeEntry.grid(row=0, column=1)
        
        # Notas
        noteFrame = Frame(self.frame, padding=[20])
        noteFrame.grid(row=1, column=0, columnspan=12)

        self.generateNotesFrame(noteFrame)

    def generateNotesFrame(self, root: Frame) -> None:
        '''Cria o componente de criação, edição e remoção de notas e ângulos'''
        # Ângulos
        self.angulosLabel = Label(root, text="Ângulos")
        self.angulosLabel.pack(anchor='nw', expand=True)        

        ## Ângulo Inicial
        self.anguloInicialEntry = Spinbox(root,
            from_= -359, to=360,
            wrap=True, textvariable=self.data.angulo_inicial,
            validate='focusout', validatecommand=(self.tk.register(validateAngle), '%P'),
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
        '''Gera um componente com uma nota com valores padrões'''
        nota = self.data.NullNote()
        self.generateNote(root, nota)
        self.data.addNote(nota["angulo"], nota["id"])
    
    def generateNote(self, root: Frame, nota):
        '''
        Cria os componentes de GUI para uma nota passada
        :nota: nota no formato {"id", "angulo"}
        '''
        frame = Frame(root, padding=[0,20, 0, 0])
        frame.pack(side=LEFT, anchor='w')
        self.noteFrames.append(frame)

        combobox = Combobox(frame, textvariable=nota["id"],
            width=4, height=5,
            values=self.controller.getPossibleNotes(), validate='all',
            validatecommand=(self.tk.register(lambda v: v in self.controller.getPossibleNotes() + [""]), '%P'))
        combobox.grid(row=0, column=0)

        spinbox = Spinbox(frame,
            from_= -359, to=360,
            wrap=True, textvariable=nota["angulo"],
            validate='all', validatecommand=(self.tk.register(validateAngle), '%P'),
            width=5
            )
        spinbox.grid(row=1, column=1)

    def deleteNote(self):
        '''Destroi os componentes GUI da nota e remove da lista'''
        self.data.deleteNote()
        frame:Frame = self.noteFrames.pop()
        frame.destroy()

