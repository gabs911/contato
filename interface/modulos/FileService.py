import json
from lib2to3.pgen2.grammar import opmap
from os import listdir, path, remove


class FileService:
    NOTE_PRESET_LOCATION = "resources/presets/notas/"
    ACCEL_PRESET_LOCATION = "resources/presets/acelerometro/"
    MAP_NOTES_LOCATION = "resources/map_notas.json"
    
    def __init__(self) -> None:
        self.ACCEL_PRESET_NAMES = filter(self.isJson, listdir(self.ACCEL_PRESET_LOCATION))
        self.NOTE_PRESET_NAMES = filter(self.isJson, listdir(self.NOTE_PRESET_LOCATION))
        self.notesMapCache = None
    
    def isJson(self, s: str):
        return s.endswith(".json")

    def getAccelPresets(self) -> list:
        accel_list = []
        for name in self.ACCEL_PRESET_NAMES:
            with open(self.ACCEL_PRESET_LOCATION + name, encoding='utf-8') as jsonfile:
                accel_list.append(json.load(jsonfile))
        return accel_list

    def getNotePresets(self) -> list:
        note_list = []
        for name in self.NOTE_PRESET_NAMES:
            with open(self.NOTE_PRESET_LOCATION + name) as jsonfile:
                note_list.append(json.load(jsonfile))
        return note_list 

    def getNotasPossiveis(self):
        if(self.notesMapCache == None):
            with open(self.MAP_NOTES_LOCATION) as jsonfile:
                self.notesMapCache = json.load(jsonfile)
        return list(self.notesMapCache.keys())
    
    def getConversorDeNotas(self) -> dict:
        if(self.notesMapCache == None):
            with open(self.MAP_NOTES_LOCATION) as jsonfile:
                self.notesMapCache = json.load(jsonfile)
        return self.notesMapCache
    
    def savePresetDeNotas(self, item, nome: str) -> None:
        with open(self.NOTE_PRESET_LOCATION + nome + ".json", 'w') as jsonfile:
            json.dump(item, jsonfile, indent=3)
    
    def deleteNota(self, nome: str) -> None:
        notePath = self.NOTE_PRESET_LOCATION + nome + ".json"
        if path.exists(notePath):
            remove(notePath)
        else:
            print("Arquivo não existe")

    def saveAccelPreset(self, item, nome: str) -> None:
        with open(self.ACCEL_PRESET_LOCATION + nome + ".json", 'w') as jsonfile:
            json.dump(item, jsonfile, indent=3)

    def deleteAccel(self, nome: str) -> None:
        accelPath = self.ACCEL_PRESET_LOCATION + nome + ".json"
        if path.exists(accelPath):
            remove(accelPath)
        else:
            print("Arquivo não existe")