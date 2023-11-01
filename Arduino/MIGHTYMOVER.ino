#include <Servo.h>

Servo rc_servo;
Servo rc_esc;

int servopin = 12;
int escpin = 13;
int stop_pin = 11;
int for_pin = 10;
int angle;
int speed = 10;

void setup() {
    rc_servo.attach(servopin);
    rc_esc.attach(escpin);
    Serial.begin(9600);
}

void setAngle() {
  angle = int(Serial.readStringUntil('\n').toInt()); //read line and convert to int
  rc_servo.write(angle);
}

/*
void stopAndGo(stop, go) {
  if(stop = high)
    dont go;
  else if forward = high
    go fast;
  else 
    go slow;
}
*/

void loop() {
    setAngle();
    rc_esc.write(speed);
    Serial.println(angle);
}
