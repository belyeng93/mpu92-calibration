#include "MPU9250.h"

MPU9250 mpu;

void setup() {
    Serial.begin(115200);
    Wire.begin();
    delay(2000);

    MPU9250Setting setting;
    setting.accel_fs_sel = ACCEL_FS_SEL::A2G;
    setting.gyro_fs_sel = GYRO_FS_SEL::G250DPS;
    setting.mag_output_bits = MAG_OUTPUT_BITS::M16BITS;
    setting.fifo_sample_rate = FIFO_SAMPLE_RATE::SMPL_200HZ;
    setting.gyro_fchoice = 0x00;
    setting.gyro_dlpf_cfg = GYRO_DLPF_CFG::DLPF_41HZ;
    setting.accel_fchoice = 0x00;
    setting.accel_dlpf_cfg = ACCEL_DLPF_CFG::DLPF_45HZ;

    if (!mpu.setup(0x68, setting)) {  // change to your own address
        while (1) {
            Serial.println("MPU connection failed. Please check your connection with `connection_check` example.");
            delay(5000);
        }
    }
}

void loop() {
    if (mpu.update()) {
        print_all();
    }
}

void print_all() {
    Serial.print(mpu.getAccX(), 2);
    Serial.print(",");
    Serial.print(mpu.getAccY(), 2);
    Serial.print(",");
    Serial.print(mpu.getAccZ(), 2);
    Serial.print(",");
    
    Serial.print(mpu.getGyroX(), 2);
    Serial.print(",");
    Serial.print(mpu.getGyroY(), 2);
    Serial.print(",");
    Serial.print(mpu.getGyroZ(), 2);
    Serial.print(",");

    Serial.print(mpu.getMagX(), 2);
    Serial.print(",");
    Serial.print(mpu.getMagY(), 2);
    Serial.print(",");
    Serial.println(mpu.getMagZ(), 2);
    // delay(100);
}
