import serial
import mido
import time
import rtmidi

serialPort = serial.Serial(port = "COM3", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ''

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(1)



#Sensor variables
gyro = 0
accel = 0
touch = 0

#variables
note = 0
last_note = 60
notes = [60,62,64,65]
notes_delay = [0,0,0,0]
lastDebounceTime = 0  
debounceDelay = 0.1
noteHold = 0.2
soundEffectDuration = 0.7
previousSoundEffect = 0
soundeEffectInterval = 1
previousSoundEffectActiv = 0


def getSensorData():
    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        sensorData = (serialString.decode('utf-8')).split('/')

        # Print the contents of the serial data
        return sensorData[0],sensorData[1],sensorData[2]

def assignTimes(note):
    if(note == 60):
        notes_delay[0] = time.time()
    elif(note == 62):
        notes_delay[1] = time.time()
    elif(note == 64):
        notes_delay[2] = time.time()
    elif(note == 65):
        notes_delay[3] = time.time()

while(1):

    #gyro, accel, touch = getSensorData()
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        sensorData = (serialString.decode('utf-8')).split('/')

        #print(sensorData)

        # Print the contents of the serial data
        gyro = float(sensorData[0])
        accel = float(sensorData[1])
        touch = float(sensorData[2])

    if((gyro//30) == -2):
        note = ('C', 60)
    elif((gyro//30) == -1):
        note = ('D',62)
    elif((gyro//30) == 0):
        note = ('E',64)
    elif((gyro//30) == 1):
        note = ('F', 65)
    
    #print(accel)

    if(touch == 1):
        if(note != last_note or (note == last_note and((time.time() - lastDebounceTime) > debounceDelay))):
            lastDebounceTime = time.time()
            assignTimes(note[1])
            last_note = note
            print(f"On + " + str(note))
            midiout.send_message([0x90,note[1],100])
    
    for i in range(4):
        if((time.time() - notes_delay[i] > noteHold) and i != note):
           #print(f"Off + " + str(note))
           midiout.send_message([0x80,notes[i],100])
    
    if(accel > 4000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        print("ACCEL DETECTED")
        midiout.send_message([0x90,78,120])
    
    if(time.time() - previousSoundEffect >= soundEffectDuration):
        previousSoundEffect = time.time()
        print("ACCEL SOUND EFFECT OFF")
        midiout.send_message([0x80,78,120])