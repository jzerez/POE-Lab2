#include <Servo.h>

Servo tilt;
Servo pan;
const int TILT_SERVO_PIN = 3; //digtial pin #
const int PAN_SERVO_PIN = 5;  //digital pin #
const int IR_PIN = A0;        //analog pin #
const int BUTTON = 4;         //digital pin #
const int TILT_ORIGIN = 25;
const int PAN_ORIGIN = 90;


const int TILT_RANGE = 20;   //deg
const int PAN_RANGE = 20;    //deg
const int STEP_SIZE = 1;     //deg
const int COMM_TIME = 200;    //ms

void setup() {
  // Initialize Serial Port and Servos
  Serial.begin(9600);
  tilt.attach(TILT_SERVO_PIN);
  pan.attach(PAN_SERVO_PIN);
  tilt.write(TILT_ORIGIN);
  pan.write(90);
  pinMode(BUTTON, INPUT);
}

void loop() {
  // ICheck button state (bouncing doesn't matter here)
  if (digitalRead(BUTTON)) {
    // Send header info about the scan
    Serial.print(TILT_RANGE);
    Serial.print(",");
    Serial.print(PAN_RANGE);
    Serial.print(",");
    Serial.println(STEP_SIZE);

    // Iterate through scan area, take and send measurements
    for (int i = 0; i < PAN_RANGE / STEP_SIZE; i++) {
      pan.write(PAN_ORIGIN - (PAN_RANGE / 2) + (STEP_SIZE * i));
      for (int j= 0; j < TILT_RANGE / STEP_SIZE; j++) {
        // Delay to account for servo moving time, lag in serial port, etc
        tilt.write(TILT_ORIGIN - (TILT_RANGE / 2) + (STEP_SIZE * j));
        delay(COMM_TIME); 
        Serial.println(analogRead(IR_PIN));
      } 
      
    }
  } else {
    // Center the servos about origin if there is no scan being processed
    if (tilt.read() != TILT_ORIGIN) {tilt.write(TILT_ORIGIN);}
    if (pan.read() != 90) {pan.write(90);}
    
  }
}
