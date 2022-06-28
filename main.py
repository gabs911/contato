import serial
import time
import rtmidi
from threading import Thread
import multiprocessing

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(1)



class Instrument4Notes():
    
    def __init__(self, port, channel,notes):
        self.port = port
        self.serialPort = 0
        self.serialString = ''
        self.gyro = 0
        self.accel = 0
        self.touch = 0
        self.channel = channel
        

        #variables
        self.note = (0,'a')
        self.last_note = 32
        self.notes = notes
        self.notes_delay = [0] * len(self.notes)
        self.lastDebounceTime = 0  
        self.debounceDelay = 0.1
        self.noteHold = 0.2
        self.soundEffectDuration = 0.7
        self.previousSoundEffect = 0
        self.soundeEffectInterval = 1
        self.previousSoundEffectActiv = 0
        self.angle = 180
    
    def assignTimes(self,note):
        for i in range(len(self.notes)):
            
            if(note == self.notes[i]):
                #print(note,self.notes[i])
                self.notes_delay[i] = time.time()
                #print(self.notes_delay)

    def setup(self):
        self.serialPort = serial.Serial(port = self.port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        if(self.channel == 0):
            self.a = 0x90
            self.b = 0x80
        elif(self.channel == 1):
            self.a = 0x91
            self.b = 0x81

    def read(self):
        if(self.serialPort.in_waiting > 0):
            self.serialString = self.serialPort.readline()
            print(self.serialString)
            self.sensorData = (self.serialString.decode('utf-8')).split('/')
            self.id = float(self.sensorData[0])
            self.gyro = float(self.sensorData[1])
            self.accel = float(self.sensorData[2])
            self.touch = float(self.sensorData[3])

            if((self.gyro//45) == -2):
                self.note = ('D4',self.notes[0])
            elif((self.gyro//45) == -1):
                self.note = ('E4',self.notes[1])
            elif((self.gyro//45) == 0):
                self.note = ('F4',self.notes[2])
            elif((self.gyro//45) == 1):
                self.note = ('F#4', self.notes[3])
          
    
            #print(self.id)

            self.can = (self.note == self.last_note) and (time.time() - self.lastDebounceTime > 0.1)
            #print(touch)
            if(self.touch <30):
                self.touch = 1

            if(self.touch == 1):
                self.lastDebounceTime = time.time()
                if(self.note != self.last_note):
                    self.assignTimes(self.note[1])
                    self.last_note = self.note
                    print(self.a)
                    midiout.send_message([self.a,self.note[1],100])
                    #SEND MIDI
                else:
                    if(self.can == True):
                        self.last_note = self.note
                        self.assignTimes(self.note[1])
                        
                        midiout.send_message([self.a,self.note[1],100])
                        #SEND MIDI
            #print(self.notes_delay + [time.time()]) 
            
            for i in range(len(self.notes)):
                if((time.time() - self.notes_delay[i] > self.noteHold)):
                #print(f"Off + " + str(note))
                    if(self.notes[i] != self.note[1]):
                        midiout.send_message([self.b,self.notes[i],100])    
                        #print("off")
                    elif(self.touch !=1):
                        midiout.send_message([self.b,self.note[1],100])
                        #print("off" + str(time.time()))


i = Instrument4Notes("COM7",0,[1,2,3,4])
i.setup()

j = Instrument4Notes("COM4",1,[67,69,71,74])
j.setup()


while(1):
    j.read()
    
    i.read()
    


