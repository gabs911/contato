from tkinter import Event, Tk
from tkinter.font import Font
from tkinter.ttk import Button, Frame, Label, Style, Widget

class GUIView:
    BACKGROUND_FRAME = 'Background.TFrame'
    PRESET_BACKGROUND_FRAME = 'Preset.Background.TFrame'
    DEFAULT_FRAME = 'TFrame'
    
    #Tipo de controller é GUIController, não é possível restringir tipo por causa de deadlock de importações
    def __init__(self, controller):
        self.controller = controller
        self.selected = ''
        self.FrameToNotePreset = { }

    
    def show(self):
        root = Tk()
        root.title('Gruppen')
        self.generateStyles()

        rootFrame = Frame(root , padding=[10], style=self.BACKGROUND_FRAME)
        rootFrame.pack()

        self.generateNoteFrame(rootFrame)
        self.generateAccelFrame(rootFrame)
        self.generateButtons(rootFrame)

        root.mainloop()

    
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

    
    def generateNoteFrame(self, root):
        frame = Frame(root, padding=[5], style=self.PRESET_BACKGROUND_FRAME)
        frame.grid(row=0, column=0)
        for item in self.controller.getNotePresets():
            self.generateNotePreset(item, frame)

    
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
            self.selected = widget
            select(widget)

        frame = Frame(root, padding=[5], style=self.DEFAULT_FRAME)
        frame.bind('<Button-1>', (lambda e: mouseFunc(e.widget)))
        frame.pack()

        #nome do preset
        label_nome = Label(frame, text= item['nome'])
        label_nome.bind('<Button-1>', (lambda e: mouseFunc(e.widget.master)))
        label_nome.grid(row=0, column=0, columnspan=12, sticky='W')

        #valor do ângulo de inicio
        label_inicio = Label(frame, text=str(item['angulo_inicial']))
        label_inicio.grid(row=2, column=0)
        for zipper in zip(item['notas'], range(len(item['notas']))):
            nota, i = zipper
            #nome da nota
            nota_nome = Label(frame, text=nota["id"])
            nota_nome.grid(row=1, column=2*i + 1)
            #valor final do ângulo da nota
            nota_valor_final = Label(frame, text=nota['proximo_angulo'])
            nota_valor_final.grid(row=2, column=2*i + 2)
        self.FrameToNotePreset[frame] = item

    
    def generateAccelFrame(self, root):
        frame = Frame(root)
        frame.grid(row=0, column=1)
        label = Label(frame, text='Hello World')
        label.grid(row=0, column=0)

    
    def generateButtons(self, root):
        frame = Frame(root)
        frame.grid(row=0, column=2, sticky='S')
        label = Button(frame, text='Mostrar Json Selecionado', command=lambda: print(self.getSelectedNote()))
        label.grid(row=0, column=0)

    def getSelectedNote(self):
        try:
            return self.FrameToNotePreset[self.selected]
        except:
            return 'Nenhum item selecionado'

  