#include <Servo.h>

// define Input pins
#define for_pin 4     // Pin 10 input from RPi: forward
#define stop_pin 13   // Pin 11 input from RPi: stop

// define PWM pins
#define servopin 6   // Pin 12 on Arduino MEGA 2560 for PWM to servo
#define pwmPin 2      // Pin 2 on Arduino MEGA 2560 for PWM to back motors

int angle;      // Serial Angle
int speed;  // Serial Speed

// Servo Package
Servo rc_servo;
Servo pwm;

//debugging purposes
int i = 0;

void setup() {
  rc_servo.attach(servopin);
  pwm.attach(pwmPin);
  
  // PinMode of gpio pins
  pinMode(for_pin, INPUT);
  pinMode(stop_pin, INPUT);
  
  // Amount of time for red light to turn on
  delay(8000); 

  // Throttle forward
  pwm.write(135);
  delay(5000);

  // Throttle backwards
  pwm.write(45);
  delay(5000);  

  pwm.write(90); // initial pwm
  
  Serial.begin(9600);
}

void loop() {

  // apply angle function
  setAngle();

  // apply forward or stop function
  goOrNo();

  //debugPWM();

}

void setAngle() {
  angle = int(Serial.readStringUntil('\n').toInt()); //read line and convert to int
  rc_servo.write(angle);
}

void goOrNo() {
  int stopstate = digitalRead(stop_pin);
  int forstate = digitalRead(for_pin);

  if (stopstate == HIGH) {
    pwm.write(90);
    //delay(2000);
  }
  else if (forstate == HIGH) {
    pwm.write(98);
    //delay(2000);
  }
  else {
    pwm.write(90);
    //delay(2000);
  }
}

void debugPWM() {
  /*
  if (Serial.available() > 0) {
    int input = Serial.parseInt();

    // Ensure the input is within the valid range
    if (input >= 0 && input <= 180) {
      rc_servo.write(input);
      Serial.println("Servo position set to: " + String(input));
    } else {
      Serial.println("Invalid input. Servo position should be between 0 and 180.");
    }

    // Delay to avoid reading too frequently
    delay(1000);
  }
  */
  
  /*
  Serial.println(i);
  if (i%2 == 0) {
    pwm.write(35);
    rc_servo.write(90);
  }
  else {
    pwm.write(45);
    rc_servo.write(10);
  }
  delay(2000);
  i++;
  */
}