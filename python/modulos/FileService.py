import json


class FileService:
    def __init__(self) -> None:
        pass

    NOTE_PRESET_LOCATION = "resources/presets/notas"
    NOTE_PRESET_NAMES = ["teste.json", "teste2.json", "teste3.json"]

    ACCEL_PRESET_LOCATION = "resources/presets/acelerometro"
    ACCEL_PRESET_NAMES = ["vidro.json", "trovoes.json", "lucas1.json", "lucas2.json", "la.json"]
    
    def getAccelPresets(self) -> list:
        accel_list = []
        for name in self.ACCEL_PRESET_NAMES:
            with open(self.ACCEL_PRESET_LOCATION + name) as jsonfile:
                accel_list.append(json.load(jsonfile))
        return accel_list

    def getNotePresets(self) -> list:
        note_list = []
        for name in self.NOTE_PRESET_NAMES:
            with open(self.NOTE_PRESET_LOCATION + name) as jsonfile:
                note_list.append(json.load(jsonfile))
        return note_list 