import serial
import mido
import time
import rtmidi
import instruments


serialPort = serial.Serial(port = "COM3", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ''

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(1)



#Sensor variables
gyro = 0
accel = 0
touch = 0







while(1):

    #gyro, accel, touch = getSensorData()
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        sensorData = (serialString.decode('utf-8')).split('/')

        print(sensorData)

        # Print the contents of the serial data
        id = int(sensorData[0])
        gyro = float(sensorData[1])
        accel = float(sensorData[2])
        touch = float(sensorData[3])

    if(id == 1):
        instruments.instrumentTwo(gyro,accel,touch, midiout)

   