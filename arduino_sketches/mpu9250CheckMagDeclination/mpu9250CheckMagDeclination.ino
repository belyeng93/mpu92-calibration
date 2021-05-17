#include "MPU9250.h"
MPU9250 mpu; // You can also use MPU9255 as is

void setup() {
    Serial.begin(115200);
    Wire.begin();
    delay(2000);

     if (!mpu.setup(0x68)) {  // change to your own address
        while (1) {
            Serial.println("MPU connection failed. Please check your connection with `connection_check` example.");
            delay(5000);
        }
        Serial.println("MPU connection OK!");
    }
}

void loop() {
    if (mpu.update()) {
//      Serial.print(mpu.getMagX());
//      Serial.print(", ");
//      Serial.print(mpu.getMagY());
//      Serial.print(", ");
//      Serial.print(mpu.getMagZ());
//      Serial.println();

      float magDeck = sqrt(pow(mpu.getMagX(),2) + pow(mpu.getMagY(),2));
      Serial.print("Mag declination: ");
      Serial.print(magDeck);
      Serial.println();
      
    }
    delay(200);
}
