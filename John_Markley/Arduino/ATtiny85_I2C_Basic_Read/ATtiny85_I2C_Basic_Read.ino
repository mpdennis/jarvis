
#include "TinyWireS.h"                  // wrapper class for I2C slave routines

#define I2C_SLAVE_ADDR  0x27            // i2c slave address (38)
#define LED1_PIN         4              // ATtiny Pin 3
#define LED2_PIN         1              // ATtiny Pin 6

void setup(){
  pinMode(LED1_PIN,OUTPUT);             // for general DEBUG use
  pinMode(LED2_PIN,OUTPUT);             // for verification
  Blink(LED1_PIN,2);                    // show it's alive
  TinyWireS.begin(I2C_SLAVE_ADDR);      // init I2C Slave mode
}


void loop(){
  byte byteRcvd = 0;
  if (TinyWireS.available()){           // got I2C input!
    byteRcvd = TinyWireS.receive();     // get the byte from master
    TinyWireS.send(byteRcvd);           // send it back to master
    Blink(LED2_PIN,byteRcvd);                  // show we transmitted
  }
}


void Blink(byte led, byte times){ // poor man's display
  for (byte i=0; i< times; i++){
    digitalWrite(led,HIGH);
    delay (250);
    digitalWrite(led,LOW);
    delay (175);
  }
}



