import this
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
    id = 0
    gyro = 0
    accel = 0
    touch = 0
    serialport = serial.Serial()


    def __init__(self, midi_port, serial_port):
        self.midi_port = midi_port
        self.serial_port = serial_port
       
    def setSerial(self):
        self.serialport = serial.Serial(port = self.serial_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    
    def getData(self):
        if(self.serialport.in_waiting > 0):
            serialString = self.serialport.readline()
            sensorData = (serialString.decode('utf-8')).split('/')
            id = float(sensorData[0])
            gyro = float(sensorData[1])
            accel = float(sensorData[2])
            touch = float(sensorData[3])
            print(sensorData)
            return [id, gyro, accel, touch]
    
    def main(self):
        self.getData()

    


instrument1 = Instrument(midi_port, "COM11")
instrument2 = Instrument(midi_port, "COM13")
instrument1.setSerial()
instrument2.setSerial()

while(1):
    instrument1.main()
    instrument2.main()
