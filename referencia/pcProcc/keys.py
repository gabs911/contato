import serial
import mido
import time
import rtmidi

serialPort = serial.Serial(port = "COM11", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
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
notes = [60,62,64,65,67]
notes_delay = [0,0,0,0,0]
lastDebounceTime = 0  
debounceDelay = 0.1
noteHold = 0.2
soundEffectDuration = 0.7
previousSoundEffect = 0
soundeEffectInterval = 1
previousSoundEffectActiv = 0



def assignTimes(note):
    if(note == 60):
        notes_delay[0] = time.time()
    elif(note == 62):
        notes_delay[1] = time.time()
    elif(note == 64):
        notes_delay[2] = time.time()
    elif(note == 65):
        notes_delay[3] = time.time()
    elif(note == 67):
        notes_delay[4] = time.time()

while(1):

    #gyro, accel, touch = getSensorData()
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        sensorData = (serialString.decode('utf-8')).split('/')

        print(serialString)

        # Print the contents of the serial data
        id = float(sensorData[0])
        gyro = float(sensorData[1])
        accel = float(sensorData[2])
        touch = float(sensorData[3])
        #print(gyro,accel,touch)
    
    #print(accel)

    if((gyro//30) == -2):
        note = ('C', 60)
    elif((gyro//30) == -1):
        note = ('D',62)
    elif((gyro//30) == 0):
        note = ('E',64)
    elif((gyro//30) == 1):
        note = ('F', 65)
    elif((gyro//30) == 2):
        note = ('G', 67)
    
    #print(accel)

    can = (note == last_note) and (time.time() - lastDebounceTime > 0.01)
    #print(touch)
    if(touch == 1):
        lastDebounceTime = time.time()
        if(note != last_note):
            assignTimes(note[1])
            last_note = note
            midiout.send_message([0x90,note[1],100])
            print("MIDI ON" + str(time.time()))
        else:
            if(can == True):
                last_note = note
                assignTimes(note[1])
                midiout.send_message([0x90,note[1],100])
                print("MIDI ON"+ str(time.time()))
    
    for i in range(5):
        if((time.time() - notes_delay[i] > noteHold)):
           #print(f"Off + " + str(note))
            if(notes[i] != note[1]):
                midiout.send_message([0x80,notes[i],100])
            elif(touch !=1):
                midiout.send_message([0x80,note[1],100])

    
    if(accel > 6000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        print("ACCEL DETECTED")
        midiout.send_message([0x90,82,120])
    
    if(time.time() - previousSoundEffect >= soundEffectDuration):
        previousSoundEffect = time.time()
        #print("ACCEL SOUND EFFECT OFF")
        midiout.send_message([0x80,82,120])