#include <Servo.h>

Servo servo1;  // Create servo object for servo 1
Servo servo2;  // Create servo object for servo 2

#define SERVO1_PIN 9  // Pin connected to servo 1
#define SERVO2_PIN 10 // Pin connected to servo 2

int pos = 0; // Variable to store servo position

void setup() {
  servo1.attach(SERVO1_PIN); // Attach servo 1 to pin 9
  servo2.attach(SERVO2_PIN); // Attach servo 2 to pin 10
}

void loop() {
  // Sweep servos from 0 to 180 degrees
  for (pos = 0; pos <= 140; pos++) {
    servo1.write(pos); // Set position for servo 1
    servo2.write(pos); // Set position for servo 2
    delay(10);         // Wait for servos to reach position
  }
  delay(500);

  // Sweep servos back from 180 to 0 degrees
  for (pos = 140; pos >= 0; pos--) {
    servo1.write(pos); // Set position for servo 1
    servo2.write(pos); // Set position for servo 2
    delay(10);         // Wait for servos to reach position
  }
  delay(1000);
}