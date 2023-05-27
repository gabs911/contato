import json
from os import listdir, path, remove


class FileService:
    def __init__(self, appDataLocation = "") -> None:
        self.NOTE_PRESET_LOCATION = appDataLocation + "resources/presets/notas/"
        self.ACCEL_PRESET_LOCATION = appDataLocation + "resources/presets/acelerometro/"
        self.MAP_NOTES_LOCATION = "resources/map_notas.json"
        self.ACCEL_PRESET_NAMES = filter(self.isJson, listdir(self.ACCEL_PRESET_LOCATION))
        self.NOTE_PRESET_NAMES = filter(self.isJson, listdir(self.NOTE_PRESET_LOCATION))
        self.notesMapCache = None
    
    def isJson(self, s: str):
        return s.endswith(".json")

    def getAccelPresets(self) -> list:
        '''retorna os presets de acelerômetro do sistema de arquivos'''
        accel_list = []
        for name in self.ACCEL_PRESET_NAMES:
            with open(self.ACCEL_PRESET_LOCATION + name, encoding='utf-8') as jsonfile:
                accel_list.append(json.load(jsonfile))
        return accel_list

    def getNotePresets(self) -> list:
        '''retorna os presets de notas do sistema de arquivos'''
        note_list = []
        for name in self.NOTE_PRESET_NAMES:
            with open(self.NOTE_PRESET_LOCATION + name) as jsonfile:
                note_list.append(json.load(jsonfile))
        return note_list 

    def getPossibleNotes(self):
        '''retorna as notas possíveis do arquivo de mapeamento de notas'''
        if(self.notesMapCache == None):
            with open(self.MAP_NOTES_LOCATION) as jsonfile:
                self.notesMapCache = json.load(jsonfile)
        return list(self.notesMapCache.keys())
    
    def getNoteConverter(self) -> dict:
        '''retorna o mapeamento de notas do sistema de arquivos'''
        if(self.notesMapCache == None):
            with open(self.MAP_NOTES_LOCATION) as jsonfile:
                self.notesMapCache = json.load(jsonfile)
        return self.notesMapCache
    
    def saveNotesPreset(self, item, nome: str) -> None:
        with open(self.NOTE_PRESET_LOCATION + nome + ".json", 'w') as jsonfile:
            json.dump(item, jsonfile, indent=3)
    
    def deleteNote(self, nome: str) -> None:
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