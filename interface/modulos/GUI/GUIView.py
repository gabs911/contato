from modulos.GUI.Components.NotePresetComponent import NotePresetComponent
from modulos.GUI.Components.PresetListComponent import PresetListComponent
from modulos.GUI.Components.AccelPresetComponent import AccelPresetComponent
from modulos.GUI.Forms.PresetFormGUI.PresetFormModule import PresetFormModule
from util.TypeCheck import isFloat
from tkinter import PhotoImage, StringVar, Tk
from tkinter.font import Font
from tkinter.ttk import Button, Combobox, Frame, Label, Spinbox, Style
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
        '''Atribui cores e estados iniciais aos componentes da interface '''
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
        '''Cria o componente da GUI da lista de presets de notas'''
        presetList = PresetListComponent(
            root, fileService=self.controller.fileService, presetList=self.controller.getNotePresets(),
            dataSetter=self.data.setNotePreset, component=NotePresetComponent)
        presetList.show(row=0, column=0)

    def generateAccelFrame(self, root):
        '''Cria o componente da GUI relacionada ao acelerômetro'''
        frame = Frame(root)
        frame.grid(row=0, column=1, padx=5)
        label = Label(frame, text='Acelerometro')
        label.grid(row=0, column=0)
        self.data.accel = StringVar(frame, "0")
        self.accel = Spinbox(frame, from_=0, to=500000,
            #a linha a seguir foi comentada porque a validação em cada frame faz com que não seja possível por valores com vírgula
            #validate='all', validatecommand=(frame.register(isFloat), '%P'),
            increment=100, 
            textvariable=self.data.accel
            )
        self.accel.grid(row=1, column=0)
        self.generateAccelPresetFrame(frame)

    def generateAccelPresetFrame(self, root):
        '''Cria o componente da GUI da lista de Presets de acelerômetro'''
        presetList = PresetListComponent(root,fileService=self.controller.fileService, presetList=self.controller.getAccelPresets(),
            dataSetter=self.data.setAccelPreset, component=AccelPresetComponent)
        presetList.show(row=2, column=0)

    def generateConnector(self, root):
        '''Cria os droplists de conexões bluetooth e conexões MIDI disponíveis'''
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
        '''Cria os botões de Tocar e Calibrar'''
        frame = Frame(root)
        frame.grid(row=1, column=2, sticky='SE')

        #Tocar
        self.data.buttonText = StringVar(root, value="Tocar")
        self.button = Button(frame, textvariable=self.data.buttonText, command=self.togglePlay)
        self.data.button = self.button
        self.button.grid(row=0, column=1)

        #Calibrar
        self.data.calibrarButtonText = StringVar(root, value="Calibrar")
        self.calibrarButton = Button(frame, textvariable=self.data.calibrarButtonText, command=self.toggleCalibration)
        self.data.calibrarButton = self.calibrarButton
        self.calibrarButton.grid(row=0, column=0)

    def togglePlay(self):
        '''Troca o estado do botão de tocando para parado ou de parado para tocando'''
        if (self.data.getPlayButtonState() == GUIButtonState.STOPED):
            if(self.data.getAccelPreset() != None) and (self.data.getNotePreset() != None):
                self.data.setPlayButtonState(GUIButtonState.STARTING)
                self.root.after(1, lambda: self.controller.start(self.root, self.getGUIInfo()))
        elif (self.data.getPlayButtonState() == GUIButtonState.RUNNING):
            self.data.setPlayButtonState(GUIButtonState.STOPED)
            self.controller.end()
    
    def toggleCalibration(self):
        '''Troca o estado do botão de calibrar de calibrando para parado ou de parado para calibrando'''
        if (self.data.getCalibrationButtonState() == GUIButtonState.STOPED):
            self.data.setCalibrationButtonState(GUIButtonState.STARTING)
            self.root.after(1, lambda: self.controller.startCalibration(self.root, self.getGUIInfo()))
        
        elif (self.data.getCalibrationButtonState() == GUIButtonState.RUNNING):
            self.data.setCalibrationButtonState(GUIButtonState.STOPED)
            self.controller.endCalibration()
    
    def getGUIInfo(self) -> GUIData:
        '''Retorna as informações do estado da GUI'''
        return self.data

  