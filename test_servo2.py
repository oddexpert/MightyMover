from gpiozero import Servo
from time import sleep

servo = Servo(12)
val = -1

LEFT = 1
RIGHT = -1
STRAIGHT = 0

try:
	servo.value = LEFT
	sleep(0.025)
	servo.value = RIGHT
	sleep(0.025)
	servo.value = STRAIGHT
	sleep(0.025)
except KeyboardInterrupt:
	print("Program stopped")
