# Import des modules
import os
import time
import ephem

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

def echoPWM(highValueMs):
  os.system("echo 2={0} > /dev/servoblaster".format(highValueMs*100))
  lastValue = highValueMs*100

def breakDoor():
  if (lastValue > int(meanDuty*100)):
    for i in reversed(range(15,int(lastValue/10))):
      #print(10*i/100.0)
      echoPWM(i/10.0)
      time.sleep(0.2)
  elif (lastValue < int(meanDuty*100)):
    for i in range(int(lastValue/10),16):
      #print(10*i/100.0)
      echoPWM(i/10.0)
      time.sleep(0.2)
  else:
    print "error in breakDoor function"

def openDoor():
  if (lastValue == 100.0):
    breakDoor(lastValue)
  for i in range(15,21):
    echoPWM(i/10.0)
    time.sleep(0.2)

def closeDoor():
  if (lastValue == 200.0):
    breakDoor(lastValue)
  for i in reversed(range(10,16)):
    echoPWM(i/10.0)
    time.sleep(0.2)

def emergencyBreakDoor():
  os.system("echo 2=150 > /dev/servoblaster")
  lastValue = 150

def readHallOpennedDoor():
  return True;
def readHallClosedDoor():
  return True;

#USAGE : 
# openDoor() activate PWM smoothly in one direction
# closeDoor() activate PWM smoothly in the other direction
# breakDoor() smoothly stop PWM
# emergencyBreakDoor() stop PWM not smoothly

o=ephem.Observer()
o.lat='48.395574'
o.long='-4.333449'
o.horizon = '-6'
etatPorte = 'fermee'
porteOuverte = readHallOpennedDoor()
porteFermee = readHallClosedDoor()

try:
  while True:
    s=ephem.Sun()
    s.compute()
    ouverturePorte =  ephem.Date(ephem.localtime(o.previous_rising(s, use_center=True)))
    fermeturePorte = ephem.Date(ephem.Date(ephem.localtime(o.next_setting(s, use_center=True))) + 15 * ephem.minute)
    maintenant = ephem.now()
    if (maintenant > ouverturePorte):
      print "Le soleil est leve, la porte doit etre ouverte"
      if (etatPorte == 'fermee'):
        openDoor()
        #on a lance l'ouverture, il faut freiner la porte si elle est ouverte
        #Switch a effet hall commande le 07/02/2016 (19 a 29jours)
        #Aimant commande le 07/02/2016 (21 a 32jours)
        while (not porteOuverte):
          time.sleep(0.01)
        breakDoor()
    elif(maintenant > fermeturePorte):
      print "Le soleil est couche, la porte doit etre fermee"
      if (etatPorte == 'fermee'):
        closeDoor()
        #on a lance la fermeture, il faut freiner la porte si elle est fermee
        #Switch a effet hall commande le 07/02/2016 (19 a 29jours)
        #Aimant commande le 07/02/2016 (21 a 32jours)
        while (not porteFermee):
          time.sleep(0.01)
        breakDoor()
except (KeyboardInterrupt, SystemExit):
  print "Arret du programme par Ctrl+c"
  raise
except:
  print "Arret du programme..."
