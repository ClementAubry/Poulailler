import sys
from threading import Thread, RLock
import time

verrou = RLock()

import RPi.GPIO as GPIO  

pinHallDoorHigh=2
pinHallDoorLow=3
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(pinHallDoorHigh, GPIO.IN)
GPIO.setup(pinHallDoorLow, GPIO.IN)
      
class doorActuatorThread(Thread):

    def echoPWM(highValueMs):
      os.system("echo 2={0} > /dev/servoblaster".format(highValueMs*100))
      lastValue = highValueMs*100
    # Define a threaded callback function to run in another thread when events are detected  
    def callbackHallDoorHigh(channel):
      print "callbackHallDoorHigh"
      if GPIO.input(pinHallDoorHigh):  
        print "La porte se ferme"
      else:  
        print "La porte est ouverte"
        echoPWM(meanDuty)

    def callbackHallDoorLow(channel):
      print "callbackHallDoorLow"
      if GPIO.input(pinHallDoorLow):  
        print "La porte s'ouvre"
      else:  
        print "La porte est fermee"
        echoPWM(meanDuty)
      
    """Thread chargé simplement d'afficher un mot dans la console."""

    def __init__(self,pinHigh,pinLow):
        Thread.__init__(self)
        self.pinLow=pinLow
        self.pinHigh=pinHigh
        GPIO.add_event_detect(pinHigh, GPIO.BOTH, callback=callbackHallDoorHigh) 
        GPIO.add_event_detect(pinLow, GPIO.BOTH, callback=callbackHallDoorLow) 

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        if (portefermee):
            echoPWM(maxDuty)
            GPIO.wait_for_edge(pinHallDoorHigh, GPIO.FALLING)
        elif(pourteouverte):
            echoPWM(minDuty)
            GPIO.wait_for_edge(pinHallDoorLow, GPIO.FALLING)
        else:
            echoPWM(meanDuty)           

# Création des threads
thread_1 = doorActuatorThread()

# Lancement des threads
thread_1.start()
thread_2.start()

# Attend que les threads se terminent
thread_1.join()
