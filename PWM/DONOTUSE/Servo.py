# Author: Ingmar Stapel 
# Usage: Servo test program
# URL: http://www.raspberry-pi-car.com/top-story-en/raspberry-pi-controlling-servo-motors/7028
# Version: 0.1 beta

import RPi.GPIO as GPIO
import time
import os

activePin=23 #la GPIO18 est sur la broche 12.http://deusyss.developpez.com/tutoriels/RaspberryPi/PythonEtLeGpio/#LII-D-1
GPIO.setwarnings(False)
# Set the layout for the pin declaration
GPIO.setmode(GPIO.BOARD)
# The pin 11 is the out pin for the PWM signal for the servo.
GPIO.setup(activePin, GPIO.OUT)

# menu info
print "l = move to the left"
print "r = move to the right"
print "m = move to the middle"
print "t = test sequence"
print "q = stop and exit"

while True:
	# Now we will start with a PWM signal at 50Hz at pin 11. 
	# 50Hz should work for many servos very will. If not you can play with the frequency if you like.
	Servo = GPIO.PWM(activePin, 50)						

	# This command sets the left position of the servo
	Servo.start(2.5)

	# Now the program asks for the direction the servo should turn.
	input = raw_input("Selection: ") 

	# You can play with the values.
	# 7.5 is in most cases the middle position
	# 12.5 is the value for a 180 degree move to the right
	# 2.5 is the value for a -90 degree move to the left
	if(input == "t"):
		print "move to the center position:"
		Servo.ChangeDutyCycle(7.5)
		time.sleep(1)
		print "move to the right position:"
		Servo.ChangeDutyCycle(12.5)
		time.sleep(1)
		print "move to the left position:"
		Servo.ChangeDutyCycle(2.5)
		time.sleep(1)
		# this stops the PWM signal
		print "Move back to start position."
		Servo.stop()

	# direction right
	if(input == "r"):

		# how many steps should the move take.
		steps = raw_input("steps (1 - 10): ") 
		print steps, "steps to the right"
		stepslength = 12.5 / int(steps)
		for Counter in range(int(steps)):
			Servo.ChangeDutyCycle(stepslength * (Counter + 1))
			print stepslength * (Counter + 1)
			time.sleep(0.5)
			
		time.sleep(1)	
		# PWM stop
		print "Move back to start position."
		Servo.stop()

	# move to the center position
	elif(input == "m"):
		print "Move back to the center position."
		Servo.start(7.5)
		time.sleep(1)
		# PWM stop
		print "Move back to start position."
		Servo.stop()
	
	# move to the left
	elif(input == "l"):
		print "Move  to the max right position and then to the left position."
		Servo.start(12.5)
		# how many steps...
		steps = raw_input("steps (1 - 10): ") 
		print steps, "steps to the right"
		stepslength = 12.5 / int(steps)
		for Counter in range(int(steps)):
			Servo.ChangeDutyCycle(12.5 - (stepslength * (Counter + 1)))
			print (12.5 - (stepslength * (Counter + 1)))
			time.sleep(0.5)
		
		time.sleep(1)
		# PWM stop
		print "Move back to start position."
		Servo.stop()
	
	# close program
	elif(input == "q"):
		print "stop the program and exit......"
		os._exit(1)
		Servo.stop()
		GPIO.cleanup()
		
	# input not valid
	else:
		print "input not valid!"
