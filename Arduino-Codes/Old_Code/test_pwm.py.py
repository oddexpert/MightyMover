import RPi.GPIO as GPIO
from time import sleep

ledpin = 12				# PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BCM)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin,500)		#create PWM instance with frequency
pi_pwm.start(0)				#start PWM of required Duty Cycle
while True:
	pi_pwm.ChangeDutyCycle(50)
"""
	for duty in range(0,100,1):
		pi_pwm.ChangeDutyCycle(duty) #provide duty cycle in the range 0-100
		sleep(0.01)
	#sleep(0.5)
	for duty in range(100,-1,-1):
		pi_pwm.ChangeDutyCycle(duty)
		sleep(0.01)
	#sleep(0.5)
"""
