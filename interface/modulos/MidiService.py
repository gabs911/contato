from rtmidi import MidiOut
from logging import getLogger
from util.logFunction import log, logException


class MidiService:
    def __init__(self) -> None:
        self.logger = getLogger("root")
        self.midiout = MidiOut()
        self.logger.info(f"portas MIDI: {self.midiout.get_ports()}")

    HEXADECIMAL_CONVERTER = {
        (0, False): 0x80,
        (0, True): 0x90,
        (1, False): 0x81,
        (1, True): 0x91,
    }

    def hexadecimalConverter(self, canal, on):
        if (canal > 15):
            self.logger.warn("Canal inválido, alterando para 15")
            canal = 15
        if (on):
            return 0x90 + canal
        else:
            return 0x80 + canal

    def listMIDIPorts(self):
        """lista as portas MIDI disponíveis"""
        return self.midiout.get_ports()

    def setup(self, port):
        """Abre uma conexão com a porta MIDI"""
        self.port = self.midiout.open_port(int(port))

    def teardown(self):
        """Fecha a conexão com a porta MIDI"""
        self.midiout.close_port()

    def send(self, canal, on, note, velocity):
        """Envia uma mensagem no canal MIDI"""
        print("teste")
        statusByte = self.hexadecimalConverter(canal, on)
        self.midiout.send_message([statusByte, note, velocity])
        self.logger.info(
            f"mensagem MIDI: canal: {canal}\nnota: {note}\non: {on}\nvelocity: {velocity}\n(statusByte): {statusByte}"
        )


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
