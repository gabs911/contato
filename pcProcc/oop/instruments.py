import serial
import mido
import time
import rtmidi



def assignTimes(note, notes_delay):
    if(note == 60):
        notes_delay[0] = time.time()
    elif(note == 62):
        notes_delay[1] = time.time()
    elif(note == 64):
        notes_delay[2] = time.time()
    elif(note == 65):
        notes_delay[3] = time.time()




def instrumentOne(gyro, accel, touch, midiout ):
    #variables
    note = (0,0)
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

    if((gyro//30) == -2):
        note = ('C', 60)
    elif((gyro//30) == -1):
        note = ('D',62)
    elif((gyro//30) == 0):
        note = ('E',64)
    elif((gyro//30) == 1):
        note = ('F', 65)
    
    #print(accel)

    can = (note == last_note) and (time.time() - lastDebounceTime > 0.2)

    if(touch == 1):
        lastDebounceTime = time.time()
        if(note != last_note):
            assignTimes(note[1],notes_delay)
            last_note = note
            midiout.send_message([0x90,note[1],100])
        else:
            if(can == True):
                last_note = note
                assignTimes(note[1],notes_delay)
                midiout.send_message([0x90,note[1],100])
    
    for i in range(4):
        if((time.time() - notes_delay[i] > noteHold)):
           #print(f"Off + " + str(note))
            if(notes[i] != note[1]):
                midiout.send_message([0x80,notes[i],100])
            elif(touch !=1):
                midiout.send_message([0x80,note[1],100])

    
    if(accel > 4000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        print("ACCEL DETECTED")
        midiout.send_message([0x90,78,120])
    
    if(time.time() - previousSoundEffect >= soundEffectDuration):
        previousSoundEffect = time.time()
        print("ACCEL SOUND EFFECT OFF")
        midiout.send_message([0x80,78,120])
    return 1

def instrumentTwo(gyro, accel, touch, midiout):
    #variables
    note = (0,0)
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

    if((gyro//30) == -2):
        note = ('C', 60)
    elif((gyro//30) == -1):
        note = ('D',62)
    elif((gyro//30) == 0):
        note = ('E',64)
    elif((gyro//30) == 1):
        note = ('F', 65)
    
    #print(accel)

    can = (note == last_note) and (time.time() - lastDebounceTime > 0.2)

    if(touch == 1):
        lastDebounceTime = time.time()
        if(note != last_note):
            assignTimes(note[1],notes_delay)
            last_note = note
            midiout.send_message([0x90,note[1],100])
        else:
            if(can == True):
                last_note = note
                assignTimes(note[1],notes_delay)
                midiout.send_message([0x90,note[1],100])
    
    for i in range(4):
        if((time.time() - notes_delay[i] > noteHold)):
           #print(f"Off + " + str(note))
            if(notes[i] != note[1]):
                midiout.send_message([0x80,notes[i],100])
            elif(touch !=1):
                midiout.send_message([0x80,note[1],100])

    
    if(accel > 4000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        print("ACCEL DETECTED")
        midiout.send_message([0x90,78,120])
    
    if(time.time() - previousSoundEffect >= soundEffectDuration):
        previousSoundEffect = time.time()
        print("ACCEL SOUND EFFECT OFF")
        midiout.send_message([0x80,78,120])