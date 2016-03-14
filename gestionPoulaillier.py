# Import des modules
import os
import time
import ephem
import RPi.GPIO as GPIO

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

pinHallDoorHigh=2
pinHallDoorLow=3
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(pinHallDoorHigh, GPIO.IN)
GPIO.setup(pinHallDoorLow, GPIO.IN)

#in milliseconds
minDuty=1
meanDuty=1.5
maxDuty=2

sens=True
dutyStep=0.5
lastValue=meanDuty 

o=ephem.Observer()
o.lat='48.395574'
o.long='-4.333449'
o.horizon = '-6'
etatPorte = 'fermee'

def echoPWM(highValueMs):
  os.system("echo 2={0} > /dev/servoblaster".format(highValueMs*100))
  lastValue = highValueMs*100

def callbackHallDoorHigh(channel):
  print "callbackHallDoorHigh"
  if GPIO.input(pinHallDoorHigh):  
    print "La porte se ferme"
  else:  
    print "La porte est ouverte"
    emergencyBreakDoor()
    etatPorte='ouverte'

def callbackHallDoorLow(channel):
  print "callbackHallDoorLow"
  if GPIO.input(pinHallDoorLow):  
    print "La porte s'ouvre"
  else:  
    print "La porte est fermee"
    breakDoor()
    etatPorte='fermee'

def openDoor():
  os.system("echo 2=200 > /dev/servoblaster")

def closeDoor():
  os.system("echo 2=100 > /dev/servoblaster")

def emergencyBreakDoor():
  os.system("echo 2=150 > /dev/servoblaster")

#USAGE : 
# openDoor() activate PWM smoothly in one direction
# closeDoor() activate PWM smoothly in the other direction
# breakDoor() smoothly stop PWM
# emergencyBreakDoor() stop PWM not smoothly

GPIO.add_event_detect(pinHallDoorHigh, GPIO.BOTH, callback=callbackHallDoorHigh) 
GPIO.add_event_detect(pinHallDoorLow, GPIO.BOTH, callback=callbackHallDoorLow) 

try:
  while True:
    s=ephem.Sun()
    s.compute()
    ouverturePorte =  ephem.Date(ephem.localtime(o.previous_rising(s, use_center=True)))
    fermeturePorte = ephem.Date(ephem.Date(ephem.localtime(o.next_setting(s, use_center=True))) + 15 * ephem.minute)
    maintenant = ephem.now()
    if (1):#(maintenant > ouverturePorte):
      print "Le soleil est leve, la porte doit etre ouverte"
      if (etatPorte == 'fermee'):
        openDoor()
        while(etatPorte == 'fermee'):
          if (GPIO.input(pinHallDoorHigh)):
            print "Atente porte ouverte"
          else:
            print "Porte ouverte"
            emergencyBreakDoor()
            etatPorte = 'ouverte'
    elif(1):#(maintenant > fermeturePorte):
      print "Le soleil est couche, la porte doit etre fermee"
      if (etatPorte == 'ouverte'):
        closeDoor()
        while(etatPorte == 'ouverte'):
          if (GPIO.input(pinHallDoorLow)):
            print "Atente porte fermee"
          else:
            print "Porte fermee"
            emergencyBreakDoor()
            etatPorte = 'fermee'
    time.sleep(10)
except (KeyboardInterrupt, SystemExit):
  GPIO.cleanup()
  print "Arret du programme par Ctrl+c"
  raise 
finally:
  GPIO.cleanup()
  print "Arret du programme..."
  raise 
