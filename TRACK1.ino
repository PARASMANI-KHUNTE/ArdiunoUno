#include <Servo.h>

Servo servo1;
Servo servo2;

void setup() {
  servo1.attach(9);  // Attach servo 1 to pin 9
  servo2.attach(10); // Attach servo 2 to pin 10
  Serial.begin(9600); // Start serial communication
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'L') {
      // Move servos to left
      servo1.write(0);   // Rotate servo 1 to 0 degrees
      //servo2.write(0);   // Rotate servo 2 to 0 degrees
    } else if (command == 'R') {
      // Move servos to right
      servo1.write(180); // Rotate servo 1 to 180 degrees
      //servo2.write(180); // Rotate servo 2 to 180 degrees
    }else if (command == 'U') {
      // Move second servo up
      servo2.write(90); // Rotate servo 2 to 90 degrees (up position)
    } else if (command == 'D') {
      // Move second servo down
      servo2.write(180); // Rotate servo 2 to 180 degrees (down position)
    }
  }
}
