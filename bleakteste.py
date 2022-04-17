import serial
import mido
import time
import rtmidi
import serial.tools.list_ports;

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
midi_port = midiout.open_port(1)

print([comport.device for comport in serial.tools.list_ports.comports()])


class Instrument:
    #Variables
    serialString = ''
    gyro = 0
    accel = 0
    touch = 0

    def __init__(self, midi_port, serialport):
        self.midi_port = midi_port
        self.serialport = serialport
    
    def getData(self, serialport):
        serialPort = serial.Serial(port = "COM12", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        if(serialPort.in_waiting > 0):
            serialString = serialPort.readline()
            sensorData = (serialString.decode('utf-8')).split('/')
            gyro = float(sensorData[0])
            accel = float(sensorData[1])
            touch = float(sensorData[2])
            print(serialString)


instrument1 = Instrument(midi_port, "COM3")



while(1):
    instrument1.getData("COM8")