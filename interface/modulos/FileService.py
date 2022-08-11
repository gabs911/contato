import json
from os import listdir


class FileService:
    NOTE_PRESET_LOCATION = "resources/presets/notas/"
    ACCEL_PRESET_LOCATION = "resources/presets/acelerometro/"
    
    def __init__(self) -> None:
        self.ACCEL_PRESET_NAMES = filter(self.isJson, listdir(self.ACCEL_PRESET_LOCATION))
        self.NOTE_PRESET_NAMES = filter(self.isJson, listdir(self.NOTE_PRESET_LOCATION))
    
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