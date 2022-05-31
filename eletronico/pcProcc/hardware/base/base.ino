/*********
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp-now-many-to-one-esp32/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*********/

#include <esp_now.h>
#include <WiFi.h>


// Structure example to receive data
// Must match the sender structure
typedef struct struct_message {
    int id; // must be unique for each sender board
    int gyro;
    int accel;
    int touch;
} struct_message;

int lastnote = 60;



// Create a struct_message called myData
struct_message MIDImessage;

// Create a structure to hold the readings from each board
struct_message board1;
struct_message board2;

// Create an array with all the structures
struct_message boardsStruct[3] = {board1, board2};

// callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac_addr, const uint8_t *incomingData, int len) {
  
  char macStr[18];
  memcpy(&MIDImessage, incomingData, sizeof(MIDImessage));
//  Serial.printf("Board ID %u: %u bytes\n", MIDImessage.id, len);
  // Update the structures with the new incoming data
  boardsStruct[MIDImessage.id-1].gyro = MIDImessage.gyro;
  boardsStruct[MIDImessage.id-1].accel = MIDImessage.accel;
  boardsStruct[MIDImessage.id-1].touch = MIDImessage.touch;

    
    Serial.println(String(MIDImessage.gyro)+'/'+String(MIDImessage.accel)+'/'+String(MIDImessage.touch));
 
}
 
void setup() {
  //Initialize Serial Monitor
  Serial.begin(115200);

  //Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  //Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  // Once ESPNow is successfully Init, we will register for recv CB to
  // get recv packer info
  esp_now_register_recv_cb(OnDataRecv);
}
 
void loop() {
  // Acess the variables for each board
//  int board1X = boardsStruct[0].x;
 // int board1Y = boardsStruct[0].y;
 // Serial.println(board1X);
//Serial.println(board1Y);
  //Serial.println(boardStruct[0].note);
  /*
  int board2X = boardsStruct[1].x;
  int board2Y = boardsStruct[1].y;
  int board3X = boardsStruct[2].x;
  int board3Y = boardsStruct[2].y;*/

  delay(10);  
}
