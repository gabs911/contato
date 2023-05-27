from rtmidi import MidiOut

class MidiService:
    def __init__(self) -> None:
        self.midiout = MidiOut()
        print(self.midiout.get_ports())
    
    HEXADECIMAL_CONVERTER = {
        (0, False): 0x80,
        (0, True): 0x90,
        (1, False): 0x81,
        (1, True): 0x91
        }

    def listMIDIPorts(self):
        '''lista as portas MIDI disponíveis'''
        return self.midiout.get_ports()
    
    def setup(self, port):
        '''Abre uma conexão com a porta MIDI'''
        self.port = self.midiout.open_port(int(port))
    
    def teardown(self):
        '''Fecha a conexão com a porta MIDI'''
        self.midiout.close_port()

    def send(self, canal, on, note, velocity):
        '''Envia uma mensagem no canal MIDI'''
        self.midiout.send_message([self.HEXADECIMAL_CONVERTER[(canal, on)], note, velocity])
        print(f"canal: {canal}\nnota: {note}\non: {on}\nvelocity: {velocity}")
        print("-----------------------------------------------------")
        pass

class MockMidiService(MidiService):
    def __init__(self) -> None:
        pass

    def setup(self, port):
        print(f"<Mock> MIDI setup for port: {port}")

    def teardown(self):
        print("<Mock> MIDI teardown")

    def send(self, canal, on, note, velocity):
        print(f"canal: {canal}\nnota: {note}\non: {on}\nvelocity: {velocity}")
        print("-----------------------------------------------------")