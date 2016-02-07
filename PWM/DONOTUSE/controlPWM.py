# Import des modules
import RPi.GPIO as GPIO
import time

# Initialisation de la numerotation et des E/S
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT, initial = GPIO.LOW)

tHMinMs=1.0
tHMaxMs=2.0
tHMeanMs=1.5
freq=50
#dutyPercent=freq*tH*10^3
def computeDutyPercent(freqHz,tMs):
	return freqHz*tMs/10

print "frequency=",freq
minDuty = computeDutyPercent(freq,tHMinMs)
print "minDutyPercent=",minDuty
meanDuty = computeDutyPercent(freq,tHMeanMs)
print "meanDutyPercent=",meanDuty
maxDuty = computeDutyPercent(freq,tHMaxMs)
print "maxnDutyPercent=",maxDuty

sens = True
dutyStep=0.5

p = GPIO.PWM(12, freq)
rapport=meanDuty
p.start(rapport) #ici, rapport vaut meanDuty

print "l = move to the left"
print "r = move to the right"
print "m = move to the middle"
print "t = test sequence"
print "q = stop and exit"


# On fait varier l'intensite de la LED
while True:
    input = raw_input("Selection: ")
    if(input == "t"):
	    rapport=minDuty
            p.ChangeDutyCycle(rapport)
            time.sleep(0.25)
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
		    p.ChangeDutyCycle(rapport)
		    time.sleep(0.25)
            p.ChangeDutyCycle(meanDuty)
            time.sleep(0.25)
    elif(input == "m"):
	    p.ChangeDutyCycle(meanDuty)
    elif(input == "l"):
	    p.ChangeDutyCycle(minDuty)
    elif(input == "r"):
	    p.ChangeDutyCycle(maxDuty)
    # close program
    elif(input == "q"):
            print "stop the program and exit......"
            GPIO.cleanup()
            os._exit(1)
    else:
	    print "input not valid!"
    time.sleep(0.25)

