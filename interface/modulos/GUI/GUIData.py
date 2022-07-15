

class GUIData:
    accel = 0
    accelPreset = None
    notePreset = None
    
    def __init__(self) -> None:
        pass
    
    def getAccel(self):
        return self.accel

    def getAccelPreset(self):
        if(self.accelPreset == None):
            print("Nenhum preset de acelerômetro selecionado")
        return self.accelPreset

    def getNotePreset(self):
        if(self.notePreset == None):
            print("Nenhum preset de nota selecionado")
        return self.notePreset
