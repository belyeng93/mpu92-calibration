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
//TODO: send data serial separated by dot comma 
void loop() {
    if (mpu.update()) {
        Serial.print(mpu.getAccX());
        Serial.print(", ");
        Serial.print(mpu.getAccY());
        Serial.print(", ");
        Serial.print(mpu.getAccZ());
        Serial.println();
        delay(1000);
    }
}
