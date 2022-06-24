from rtmidi import MidiOut

class MidiService:
    def __init__(self, port) -> None:
        self.midiout = MidiOut()
        print(self.midiout.get_ports())
        self.port = self.midiout.open_port(port)
        pass
    
    CONVERSOR_HEXADECIMAL = {
        (0, True): 0x80,
        (0, False): 0x90,
        (1, True): 0x81,
        (1, False): 0x91
        }

    def send(self, canal, on, note, velocity):
        self.midiout.send_message(self.CONVERSOR_HEXADECIMAL[(canal, on)], note, velocity)
        pass

class MockMidiService(MidiService):
    def __init__(self) -> None:
        pass

    def send(self, canal, on, note, velocity):
        print(f"canal: {canal}\nnota: {note}\non: {on}\nvelocity: {velocity}")
        print("-----------------------------------------------------")