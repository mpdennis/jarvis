// ATTiny based I2C control
// Needs th TinyWireS library
 
#include "TinyWireS.h"                  // wrapper class for I2C slave routines
 
#define I2C_SLAVE_ADDR  0x30             // i2c slave address
#define Relay1_PIN  1
#define Relay2_PIN  4
#define Relay3_PIN  3
 
void setup(){
  pinMode(Relay1_PIN,OUTPUT);
  pinMode(Relay2_PIN,OUTPUT);
  pinMode(Relay3_PIN,OUTPUT);
  TinyWireS.begin(I2C_SLAVE_ADDR);      // init I2C Slave mode
}
 
void loop(){
  byte byteRcvd = 0;//channel
  byte byteRcvd1 = 0;//option1 - on/off/dimval
  
  if (TinyWireS.available()){           // got I2C input!
    byteRcvd = TinyWireS.receive();     // get first byte from master
    byteRcvd1 = TinyWireS.receive();    // get second byte from master
      switch (byteRcvd) {
        case 0x01:
          Switch(Relay2_PIN);
        break;
        case 0x02:
          Switch(Relay2_PIN);
        break;
        case 0x03:
          Switch(Relay3_PIN);
          //Dimmer(byteRcvd1);
        break;
        
        
        case 0x13:
          digitalWrite(Relay3_PIN, byteRcvd1);
        break;
        case 0x23:
          Dimmer(byteRcvd1);
        break;
        case 0x33:
          Dimmer2(byteRcvd1);//
        break;
      }
 
  }
}

void Switch(int relay){
    if (digitalRead(relay) == HIGH){ digitalWrite(relay,LOW);}
    else {digitalWrite(relay,HIGH);}
}

void OnOff(int relay,int State){
    if (State == 0){ digitalWrite(relay,LOW);}
    else {digitalWrite(relay,HIGH);}
}
void Dimmer2(int dimmerval){
analogWrite(1, dimmerval);
}
void Dimmer(int dimmerval){
    switch (dimmerval){
       case 0x00:
         analogWrite(1, 0);
         break;
       case 0x01:
         analogWrite(1, 50);
         break;
       case 0x02:
         analogWrite(1, 100);
         break;       
       case 0x03:
         analogWrite(1, 230);
         break;
       case 0x04:
         analogWrite(1, 240);
         break;
       case 0x05:
         analogWrite(1, 250);
         break;
    }
}
