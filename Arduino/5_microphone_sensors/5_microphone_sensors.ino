#include <Wire.h>

const int numSensors = 5;   // Number of microphone sensors
const int multiplexerAddress = 0x20;  // I2C address of the multiplexer

void setup() {
  Serial.begin(9600);   // Initialize serial communication
  Wire.begin();   // Initialize I2C communication

  // Set the multiplexer pins as outputs
  for (int i = 0; i < numSensors; i++) {
    pinMode(i, OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < numSensors; i++) {
    // Select a microphone sensor
    selectSensor(i);

    int sensorValue = analogRead(A0);  // Read the analog value from the ADC

    // Send the sensor index and value to the computer
    Serial.print("Sensor ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(sensorValue);

    // Deselect the microphone sensor
    deselectSensor();
  }

  // delay(10);   // Delay between readings
}

void selectSensor(int sensorIndex) {
  Wire.beginTransmission(multiplexerAddress);  // Begin I2C communication with the multiplexer
  Wire.write(1 << sensorIndex);  // Send the corresponding bit pattern to select the sensor
  Wire.endTransmission();  // End I2C communication
}

void deselectSensor() {
  Wire.beginTransmission(multiplexerAddress);  // Begin I2C communication with the multiplexer
  Wire.write(0x00);  // Send 0x00 to deselect all sensors
  Wire.endTransmission();  // End I2C communication
}
