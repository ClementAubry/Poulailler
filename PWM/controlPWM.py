# Import des modules
import os
import time

#Inspired from http://stephane.lavirotte.com/perso/rov/esc_brushless_raspberry.html
# with GPIO mapping here : http://deusyss.developpez.com/tutoriels/RaspberryPi/PythonEtLeGpio/#LII-D
#Servo mapping:
#0 on P1-7 GPIO-4
#1 on P1-11 GPIO-17
#2 on P1-12 GPIO-18
#3 on P1-13 GPIO-21
#4 on P1-15 GPIO-22
#5 on P1-16 GPIO-23
#6 on P1-18 GPIO-24
#7 on P1-22 GPIO-25

#in milliseconds
minDuty=1
meanDuty=1.5
maxDuty=2

sens=True
dutyStep=0.5
lastValue=meanDuty

def breakDoor(lastVal):
	if (lastVal > int(meanDuty*100)):
		for i in reversed(range(15,int(lastVal/10))):
			print(10*i/100.0)
			lastVal = echoPWM(i/10.0)
			time.sleep(0.2)
	elif (lastVal < int(meanDuty*100)):
		for i in range(int(lastVal/10),16):
			print(10*i/100.0)
			lastVal = echoPWM(i/10.0)
			time.sleep(0.2)
	else:
		print "error in breakDoor function"
	return lastVal

def echoPWM(highValueMs):
	os.system("echo 2={0} > /dev/servoblaster".format(highValueMs*100))
	return highValueMs*100

def openDoor():
	if (lastValue == 100.0):
		breakDoor(lastValue)
	for i in range(15,21):
		l = echoPWM(i/10.0)
		time.sleep(0.2)
		print(i/10.0)
	return i*10
		
def closeDoor():
	if (lastValue == 200.0):
		breakDoor(lastValue)
	for i in reversed(range(10,16)):
		l = echoPWM(i/10.0)
		time.sleep(0.2)
		print(i/10.0)
	return i*10

print "l = move to the left"
print "r = move to the right"
print "m = move to the middle"
print "o = open the door"
print "p = close the door"
print "t = test sequence"
print "q = stop and exit"

#Boucle principale
while True:
	input = raw_input("Selection: ")
	if(input == "t"):
		rapport=minDuty
		echoPWM(rapport)
		for Counter in range(10):
			if sens and rapport < maxDuty:
				rapport += dutyStep
			elif sens and rapport >= maxDuty:
				sens = False
			elif not sens and rapport > minDuty:
				rapport -= dutyStep
			elif rapport == minDuty:
				sens = True
			print(rapport)
			lastValue = echoPWM(rapport)
			time.sleep(0.25)
	elif(input == "m"):
		lastValue = echoPWM(meanDuty)
	elif(input == "l"):
		lastValue = echoPWM(minDuty)
	elif(input == "r"):
		lastValue = echoPWM(maxDuty)
	elif(input == "o"):
		lastValue = openDoor()
	elif(input == "p"):
		lastValue = closeDoor()

	elif(input == "b"):
		lastValue = breakDoor(lastValue)
	# close program
	elif(input == "q"):
		print "stop the program and exit......"
		echoPWM(meanDuty)
		os._exit(1)
	else:
		print "input not valid!"
	time.sleep(0.25)
	print(lastValue)
