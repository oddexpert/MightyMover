from gpiozero import Servo
from time import sleep

servo = Servo(12)
val = -1

LEFT = 0.75
RIGHT = -0.75
STRAIGHT = 0

try:
	while True:
		servo.value = STRAIGHT
		sleep(0.5)
		servo.value = LEFT
		sleep(0.5)
		servo.value = RIGHT
		sleep(0.5)
except KeyboardInterrupt:
	print("Program stopped")
