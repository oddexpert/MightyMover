from gpiozero import Servo
from time import sleep

servo = Servo(13)
val = -1

FORWARDS = -0.13
BACK = -0.4
STOP = -0.35

try:
	servo.value = BACK
	sleep(2)
except KeyboardInterrupt:
	print("Program stopped")
