import this
import serial
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
    elif(note == 67):
        notes_delay[4] = time.time()


class EletronicModule:

    def __init__(self,porta):
        self.porta = porta
    
    def setup(self):
        self.serialPort = serial.Serial(port = self.porta , baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        self.midiout = rtmidi.MidiOut()
        self.port = self.midiout.open_port(1)
        print("Setup done")

    def getData(self):

        if(self.serialPort.in_waiting > 0):
            serialString = (self.serialPort.readline())
            sensorData = (serialString.decode('utf-8')).split('/')
            #print(sensorData[1])
            self.gyro = float(sensorData[1])
            self.accel = float(sensorData[2])
            self.touch = int(sensorData[3])

class instrumento(EletronicModule):

    def __init__(self, porta):
        super().__init__(porta)
        self.note = 0
        self.last_note = 60
        self.notes = [60,62,64,65,67]
        self.notes_delay = [0,0,0,0,0]
        self.lastDebounceTime = 0  
        self.debounceDelay = 0.1
        self.noteHold = 0.2
        self.soundEffectDuration = 0.7
        self.previousSoundEffect = 0
        self.soundeEffectInterval = 1
        self.previousSoundEffectActiv = 0
        self.accel = 0
        self.gyro = 0
        self.touch = 0
        self.stopVar = False
        self.lastExec = 0
    
    def main(self):

        while(self.stopVar == False):
            if(time.time()- self.lastExec > 0.02):
                self.getData()
                print(self.touch)
                #print(sensorData)
                #sensorData = (sensorData.decode('utf-8')).split('/')
                #self.gyro = sensorData[1]
                #self.accel = sensorData[2]
                #self.touch = sensorData[3]
                if((self.gyro//30) == -2):
                    self.note = ('C', 60)
                elif((self.gyro//30) == -1):
                    self.note = ('D',62)
                elif((self.gyro//30) == 0):
                    self.note = ('E',64)
                elif((self.gyro//30) == 1):
                    self.note = ('F', 65)
                elif((self.gyro//30) == 2):
                    self.note = ('G', 67)
                
                #print(accel)
                
                self.can = (self.note == self.last_note) and (time.time() - self.lastDebounceTime > 0.01)
                #print(touch)
                if(self.touch == 1):
                    self.lastDebounceTime = time.time()
                    if(self.note != self.last_note):
                        assignTimes(self.note[1], self.notes_delay)
                        self.last_note = self.note
                        self.midiout.send_message([0x90,self.note[1],100])
                        #print("MIDI ON" + str(time.time()))
                    else:
                        if(self.can == True):
                            self.last_note = self.note
                            assignTimes(self.note[1],self.notes_delay)
                            self.midiout.send_message([0x90,self.note[1],100])
                            #print("MIDI ON"+ str(time.time()))
                
                for i in range(5):
                    if((time.time() - self.notes_delay[i] > self.noteHold)):
                    #print(f"Off + " + str(note))
                        if(self.notes[i] != self.note[1]):
                            self.midiout.send_message([0x80,self.notes[i],100])
                        elif(self.touch !=1):
                            self.midiout.send_message([0x80,self.note[1],100])

                
                if(self.accel > 6000 and (time.time() - self.previousSoundEffectActiv >= self.soundeEffectInterval)):
                    self.previousSoundEffectActiv = time.time()
                    print("ACCEL DETECTED")
                    self.midiout.send_message([0x90,82,120])
                
                if(time.time() - self.previousSoundEffectActiv >= self.soundEffectDuration):
                    self.previousSoundEffect = time.time()
                    #print("ACCEL SOUND EFFECT OFF")
                    self.midiout.send_message([0x80,82,120])
                
                self.lastExec = time.time()
    
    def stop(self):
        self.stopVar = True
        


modulo = instrumento("COM7")

modulo.setup()

while(1):
    modulo.main()
  