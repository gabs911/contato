from modulos.GUI.PresetFormGUI.PresetFormData import PresetFormData
from modulos.GUI.PresetFormGUI.PresetFormModule import PresetFormModule
from util.TypeCheck import isInt
from util.Event import SimpleEvent
from tkinter import BOTTOM, LEFT, RIGHT, PhotoImage, StringVar, Tk, messagebox
from tkinter.font import Font
from tkinter.ttk import Button, Combobox, Entry, Frame, Label, Spinbox, Style, Widget
from modulos.GUI.GUIData import GUIButtonState

from modulos.GUI.GUIController import GUIController
from modulos.GUI.GUIData import GUIData

class GUIView:
    BACKGROUND_FRAME = 'Background.TFrame'
    PRESET_BACKGROUND_FRAME = 'Preset.Background.TFrame'
    DEFAULT_FRAME = 'TFrame'
    DELETE_BUTTON = 'Delete.TButton'
    
    def __init__(self, controller: GUIController, presetFormModule: PresetFormModule):
        self.controller = controller
        self.presetForm = presetFormModule
        self.selected = ''
        self.selectedAccelPreset = ''
        self.FrameToNotePreset = { }
        self.FrameToAccelPreset = { }
        self.data = GUIData()
        
    
    def show(self):
        self.root = Tk()
        self.root.title('Gruppen - Contato')
        self.root.geometry("")
        self.generateStyles()

        rootFrame = Frame(self.root , padding=[10], style=self.BACKGROUND_FRAME)
        rootFrame.pack()

        self.generateNoteFrame(rootFrame)
        self.generateAccelFrame(rootFrame)
        self.generateConnector(rootFrame)
        self.generateButtons(rootFrame)

        self.root.mainloop()

    def generateStyles(self):
        style = Style()
        style.configure(self.BACKGROUND_FRAME, background='white')
        style.configure(self.PRESET_BACKGROUND_FRAME, background='black')
        style.configure(self.DEFAULT_FRAME, background='gray')
        style.map(self.DEFAULT_FRAME, background=[('selected', 'yellow')])
        style.configure('TLabel', background='gray', foreground='white', font=Font(family='Arial', size=30))
        style.map('TLabel', 
            background=[('selected', 'yellow')], 
            foreground=[('selected', 'black')]
        )
        self.delete_image = PhotoImage(file="resources/imagens/trash.png")

    def generateNoteFrame(self, root):

        frame = Frame(root, padding=[5], style=self.PRESET_BACKGROUND_FRAME)
        frame.grid(row=0, column=0)
        for item in self.controller.getNotePresets():
            self.generateNotePreset(item, frame)

        addButton = Button(frame, padding=[5], text="+",
                command=lambda: self.generateCreateNoteForm(frame))
        addButton.pack(anchor='s', side=BOTTOM)

    def generateNotePreset(self, item, root):       
        def select(widget: Widget):
            widget.state(['selected'])
            for child in widget.children.values():
                select(child)
        
        def unselect(widget: Widget):
            widget.state(['!selected'])
            for child in widget.children.values():
                unselect(child)
       
        def mouseFunc(widget: Widget):
            if (type(self.selected) == Frame):
                unselect(self.selected)
            self.data.notePreset = self.FrameToNotePreset[widget]
            self.selected = widget
            select(widget)

        frame = Frame(root, padding=[5], style=self.DEFAULT_FRAME)
        frame.pack(fill='x')

        #frame para o preset da nota
        noteFrame = Frame(frame, style=self.DEFAULT_FRAME)
        noteFrame.bind('<Button-1>', (lambda e: mouseFunc(e.widget)))
        noteFrame.pack(fill='x', expand=True, anchor='w', side=LEFT)
        
        #nome do preset
        label_nome = Label(noteFrame, text=item['nome'])
        label_nome.bind('<Button-1>', (lambda e: mouseFunc(e.widget.master)))
        label_nome.grid(row=0, column=0, columnspan=12, sticky='W')

        #valor do ângulo de inicio
        label_inicio = Label(noteFrame, text=str(item['angulo_inicial']))
        label_inicio.grid(row=2, column=0)
        for zipper in zip(item['notas'], range(len(item['notas']))):
            nota, i = zipper
            #nome da nota
            nota_nome = Label(noteFrame, text=nota["id"])
            nota_nome.grid(row=1, column=2*i + 1)
            #valor final do ângulo da nota
            nota_valor_final = Label(noteFrame, text=nota['proximo_angulo'])
            nota_valor_final.grid(row=2, column=2*i + 2)
        #adiciona no map para ser encontrável depois
        self.FrameToNotePreset[noteFrame] = item

        self.generateNoteFrameButtons(frame, noteFrame, root, item)

    def generateNoteFrameButtons(self, frame, noteFrame, root, item) -> None:
        buttonFrame = Frame(frame, style=self.DEFAULT_FRAME)
        buttonFrame.pack(anchor='e', side=RIGHT)
        
        #adiciona botão de editar
        edit_button = Button(buttonFrame, text="Editar", command=lambda: self.generateEditNoteForm(root, noteFrame), width=6)
        edit_button.grid(row=0, column=0)

        #adiciona botão de deletar
        delete_button = Button(buttonFrame, image=self.delete_image, command=lambda: self.deleteNoteForm(noteFrame))
        delete_button.grid(row=0, column=1)
        

    def generateCreateNoteForm(self, root: Frame, data = None):
        self.formEvent = SimpleEvent()
        self.formEvent.add_listenter(lambda preset: self.generateNotePreset(preset, root))
        self.formEvent.add_listenter(lambda preset: self.controller.savePresetDeNotas(preset, preset["nome"]))
        self.formView = self.presetForm.createView(self.root, self.formEvent, data)
        self.formView.show()
    
    def generateEditNoteForm(self, root: Frame, noteFrame: Frame):
        item = self.FrameToNotePreset[noteFrame]
        data = PresetFormData(item)
        self.formEvent = SimpleEvent()
        self.formEvent.add_listenter(lambda _: self.deleteNote(item, noteFrame))
        self.formEvent.add_listenter(lambda preset: self.generateNotePreset(preset, root))
        self.formEvent.add_listenter(lambda preset: self.controller.savePresetDeNotas(preset, preset["nome"]))
        self.formView = self.presetForm.createView(self.root, self.formEvent, data)
        self.formView.show()
        
    def deleteNoteForm(self, noteFrame: Frame) -> None:
        item = self.FrameToNotePreset[noteFrame]
        confirmacao = messagebox.askokcancel(
            title="Confimação de deleção",
            message=f"Tem certeza que deseja deletar o preset \"{item['nome']}\"?",
            icon=messagebox.WARNING
            )
        if confirmacao:
            self.deleteNote(item, noteFrame)
    
    def deleteNote(self, item, noteFrame: Frame) -> None:
        print(item)
        self.FrameToNotePreset.pop(noteFrame)
        self.controller.fileService.deleteNota(item["nome"])
        noteFrame.master.pack_forget()
        noteFrame.master.destroy()

    def generateAccelFrame(self, root):
        frame = Frame(root)
        frame.grid(row=0, column=1, padx=5)
        label = Label(frame, text='Acelerometro')
        label.grid(row=0, column=0)
        self.data.accel = StringVar(frame, "0")
        #self.accel = StringVar(root, value="2")
        self.accel = Spinbox(frame, from_=0, to=500000,
            validate='all', validatecommand=(frame.register(isInt), '%P'),
            increment=100, width=15,
            textvariable=self.data.accel
            )
        self.accel.grid(row=1, column=0)
        self.generateAccelPresetFrame(frame)

    def generateAccelPresetFrame(self, root):
        frame = Frame(root, padding=[5], style=self.PRESET_BACKGROUND_FRAME)
        frame.grid(row=2, column=0)
        for item in self.controller.getAccelPresets():
            self.generateAccelPreset(frame, item)

    def generateAccelPreset(self, root, item):
        def select(widget: Widget):
            widget.state(['selected'])
            for child in widget.children.values():
                select(child)
        
        def unselect(widget: Widget):
            widget.state(['!selected'])
            for child in widget.children.values():
                unselect(child)
       
        def mouseFunc(widget: Widget):
            if (type(self.selectedAccelPreset) == Frame):
                unselect(self.selectedAccelPreset)
            self.data.accelPreset = self.FrameToAccelPreset[widget]
            self.selectedAccelPreset = widget
            select(widget)
        
        frame = Frame(root, padding=[5], style=self.DEFAULT_FRAME)
        frame.bind('<Button-1>', (lambda e: mouseFunc(e.widget)))
        frame.pack(fill='x')

        #nome do preset
        label_nome = Label(frame, text= item['nome'])
        label_nome.bind('<Button-1>', (lambda e: mouseFunc(e.widget.master)))
        # label_nome.grid(row=0, column=0, sticky='W')
        label_nome.pack(anchor='nw', side=LEFT)

        label_valor = Label(frame, text=item["nota"], justify='right', padding=[0,20,0,0])
        label_valor.bind('<Button-1>', (lambda e: mouseFunc(e.widget.master)))
        # label_valor.grid(row=1, column=1, sticky='E')
        label_valor.pack(anchor='se', side=RIGHT)

        self.FrameToAccelPreset[frame] = item

    def generateConnector(self, root):
        frame = Frame(root)
        frame.grid(row=0, column=2)

        #Bluetooth
        label = Label(frame, text="Porta Bluetooth")
        label.grid(row=0, column=0, columnspan=2, sticky="w")

        self.data.COMText = StringVar(root, "")
        combobox = Combobox(frame, textvariable=self.data.COMText,
            values=self.controller.listCOMPorts(),
            width=16
            )
        combobox.grid(row=1,column=0)
        refreshButton = Button(frame, text="R",
            width=2,
            command=lambda: combobox.config(values=self.controller.listCOMPorts())
            )
        refreshButton.grid(row=1, column=1)

        #MIDI
        label = Label(frame, text="Porta MIDI")
        label.grid(row=2, column=0, sticky="w")
        self.data.MIDIText = StringVar(root, "")

        MIDIcombobox = Combobox(frame, textvariable=self.data.MIDIText,
            values=self.controller.listMIDIPorts(),
            width=16
            )
        MIDIcombobox.grid(row=3,column=0)
        MIDIrefreshButton = Button(frame, text="R",
            width=2,
            command=lambda: MIDIcombobox.config(values=self.controller.listMIDIPorts())
            )
        MIDIrefreshButton.grid(row=3, column=1)

    
    def generateButtons(self, root):
        frame = Frame(root)
        frame.grid(row=1, column=2, sticky='SE')

        #Tocar
        self.data.buttonText = StringVar(root, value="Tocar")
        self.button = Button(frame, textvariable=self.data.buttonText, command=self.toggleTocar)
        self.data.button = self.button
        self.button.grid(row=0, column=1)

        #Calibrar
        self.data.calibrarButtonText = StringVar(root, value="Calibrar")
        self.calibrarButton = Button(frame, textvariable=self.data.calibrarButtonText, command=self.toggleCalibrar)
        self.data.calibrarButton = self.calibrarButton
        self.calibrarButton.grid(row=0, column=0)

    def toggleTocar(self):
        if (self.data.buttonText.get() == "Tocar"):
            guiInfo = self.getGUIInfo()
            if(guiInfo.getAccelPreset != None) and (guiInfo.getNotePreset() != None):
                self.data.setButtonState(GUIButtonState.INICIANDO)
                self.root.after(1, lambda: self.controller.start(self.root, self.getGUIInfo()))
        elif (self.data.buttonText.get() == "Parar"):
            self.data.setButtonState(GUIButtonState.PARADO)
            self.controller.end()
    
    def toggleCalibrar(self):
        if (self.data.calibrarButtonText.get() == "Calibrar"):
            self.data.setCalibrarState(GUIButtonState.INICIANDO)
            self.root.after(1, lambda: self.controller.startCalibrar(self.root, self.getGUIInfo()))
        
        elif (self.data.calibrarButtonText.get() == "Parar"):
            self.data.setCalibrarState(GUIButtonState.PARADO)
            self.controller.endCalibrar()
    
    def getGUIInfo(self) -> GUIData:
        return self.data

  