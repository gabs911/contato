from tkinter import Tk
from modulos.GUI.Forms.FormController import FormController
from modulos.GUI.Forms.FormView import FormView
from modulos.GUI.Forms.FormData import FormData
from util.Event import SimpleEvent
from util.logFunction import log, logException


class FormModule:
    '''Esqueleto para o módulo de criação e edição dos presets'''
    def __init__(self) -> None:
        pass

    def createView(self, tk: Tk, event: SimpleEvent, data: FormData) -> FormView:
        '''Cria a janela para a criação dos presets'''
        pass

    @logException
    def getController(self) -> FormController:
        '''Retorna o controlador criado para a janela de criação/edição dos presets'''
        try:
            return self.controller
        except:
            return None