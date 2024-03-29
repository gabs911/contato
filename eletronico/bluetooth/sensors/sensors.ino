//LIBRARIES
#include "MPU6050_6Axis_MotionApps20.h"
#include <WiFi.h>
#include "BluetoothSerial.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif


BluetoothSerial SerialBT;

//MPU Initialization
MPU6050 mpu;
#define INTERRUPT_PIN 35
bool dmpReady = false;  
uint8_t mpuIntStatus;   
uint8_t devStatus;      
uint16_t packetSize;   
uint16_t fifoCount;    
uint8_t fifoBuffer[64];
Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 aa;         // [x, y, z]            accel sensor measurements
VectorInt16 aaReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 aaWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector

volatile bool mpuInterrupt = false;    
void dmpDataReady() {
    mpuInterrupt = true;
}

//ESPNOW Initialization


//Variables
float ypr_mod = 0;
int note_anterior = 60;
int note_atual = 0;
char note;
int fsrPin = 25;
int fsr =0;

int mediaAccel;


int buttonState;             // the current reading from the input pin
int lastButtonState = 0;


void setup() {
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
        Wire.setClock(400000); // 400kHz I2C clock. Comment this line if having compilation difficulties
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif
  Serial.begin(115200);
  SerialBT.begin("Contato-standalone");
  //GYRO Initialization
  Serial.println(F("Initializing I2C devices..."));
  mpu.initialize();
  pinMode(INTERRUPT_PIN, INPUT);
  Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));
  Serial.println(F("\nSend any character to begin DMP programming and demo: "));
  //while (Serial.available() && Serial.read()); // empty buffer
  //while (!Serial.available());                 // wait for data
  //while (Serial.available() && Serial.read()); // empty buffer again 
  Serial.println(F("Initializing DMP..."));
  devStatus = mpu.dmpInitialize();

  //Offsets
  mpu.setXGyroOffset(220);//220
  mpu.setYGyroOffset(76);//76
  mpu.setZGyroOffset(-85);//-85
  mpu.setZAccelOffset(1788); // 1688 factory default for my test chip
  if (devStatus == 0) {
          // Calibration Time: generate offsets and calibrate our MPU6050
          mpu.CalibrateAccel(6);
          mpu.CalibrateGyro(6);
          mpu.PrintActiveOffsets();
          // turn on the DMP, now that it's ready
          Serial.println(F("Enabling DMP..."));
          mpu.setDMPEnabled(true);
  
          // enable Arduino interrupt detection
          Serial.print(F("Enabling interrupt detection (Arduino external interrupt "));
          Serial.print(digitalPinToInterrupt(INTERRUPT_PIN));
          Serial.println(F(")..."));
          attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady, RISING);
          mpuIntStatus = mpu.getIntStatus();
  
          // set our DMP Ready flag so the main loop() function knows it's okay to use it
          Serial.println(F("DMP ready! Waiting for first interrupt..."));
          dmpReady = true;
  
          // get expected DMP packet size for later comparison
          packetSize = mpu.dmpGetFIFOPacketSize();
      } 
      else {
          // ERROR!
          // 1 = initial memory load failed
          // 2 = DMP configuration updates failed
          // (if it's going to break, usually the code will be 1)
          Serial.print(F("DMP Initialization failed (code "));
          Serial.print(devStatus);
          Serial.println(F(")"));
      }


  
}


void loop() {
  
   
    // if programming failed, don't try to do anything
    if (!dmpReady) return;
    // read a packet from FIFO
    if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) { 
      
        mpu.dmpGetQuaternion(&q, fifoBuffer);
        mpu.dmpGetGravity(&gravity, &q);
        mpu.dmpGetAccel(&aa, fifoBuffer);
        mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
        mpu.dmpGetGravity(&gravity, &q);
        mpu.dmpGetLinearAccel(&aaReal, &aa, &gravity);
        ypr_mod = ypr[2] * 180/M_PI;

      

        int pressed = touchRead();
  
    
  

        SerialBT.println("01/" + String(ypr_mod)+'/'+String(mediaAccel)+'/'+String(pressed));
        Serial.println("MIDI SENT");
        Serial.println(String(ypr_mod));




   }
   
  delay(10);
}


int touchRead()
{
  int media = 0;
  mediaAccel = 0;
  for(int i=0; i< 100; i++)
  {
    media += touchRead(T3);
    mediaAccel += aaReal.z;
    
  }
  media =  media/100;
  mediaAccel = mediaAccel/100;
  if (media < 15)
  {
    return 1;
  }
  else
  {
    return 0;
  }
}
