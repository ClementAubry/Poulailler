# Import des modules
import os
import sys
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


#On prepare un fichier temporaire tant que le script est lance
# pid = str(os.getpid())
# pidfile = "/tmp/gestionPoulaillerRunning.pid"
# if os.path.isfile(pidfile):
#   print "%s already exists, exiting" % pidfile
#   sys.exit()
# file(pidfile, 'w').write(pid)

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

def openDoor():
  os.system("echo 0=180 > /dev/servoblaster")

def closeDoor():
  os.system("echo 0=120 > /dev/servoblaster")

def emergencyBreakDoor():
  os.system("echo 0=150 > /dev/servoblaster")

def log(filename,thelog):
  os.system("echo {1} >> {0}".format(filename,thelog))


#USAGE : 
# openDoor() activate PWM smoothly in one direction
# closeDoor() activate PWM smoothly in the other direction
# breakDoor() smoothly stop PWM
# emergencyBreakDoor() stop PWM not smoothly

emergencyBreakDoor()
lastlogtime = ephem.Date(ephem.Date(ephem.localtime(ephem.now()))-59*ephem.minute)
try:
  while True:
    today = str(ephem.now()).split()[0]
    filename = today.replace("/","_")+"_poulailler.log"
    if(not GPIO.input(pinHallDoorHigh)):
      etatPorte='ouverte'
    if(not GPIO.input(pinHallDoorLow)):
      etatPorte='fermee'
    o.date=today+" 12:00:00"
    s=ephem.Sun()
    s.compute()
    ouverturePorte =  ephem.Date(ephem.localtime(o.previous_rising(s, use_center=True)))
    fermeturePorte = ephem.Date(ephem.Date(ephem.localtime(o.next_setting(s, use_center=True))) + 0 * ephem.minute)
    maintenant = ephem.Date(ephem.localtime(ephem.now()))
    if (maintenant > ouverturePorte and maintenant < fermeturePorte):
      if (etatPorte == 'fermee'):
        log(filename,"Le soleil est leve, la porte doit etre ouverte")
        log(filename,'Ouverture poulailler : ' + str(ouverturePorte))
        log(filename,'Fermeture poulailler : ' + str(fermeturePorte))
        lastlogtime=str(ephem.Date(ephem.localtime(ephem.now())))
        log(filename,'Date actuelle        : ' + lastlogtime)
        log(filename,'Etat porte           : ' + str(etatPorte)) 
        openDoor()
        log(filename,"Commande ouverture envoyee, attente ouverture")    
        while(etatPorte == 'fermee'):
          if (not GPIO.input(pinHallDoorHigh)):
            emergencyBreakDoor()
            etatPorte = 'ouverte'
            log(filename,"Porte Ouverte")
            lastlogtime=str(ephem.Date(ephem.localtime(ephem.now())))
            log(filename,'Date actuelle        : ' + lastlogtime)
            log(filename,'Etat porte           : ' + str(etatPorte)) 
    elif(maintenant > fermeturePorte or maintenant < ouverturePorte):
      if (etatPorte == 'ouverte'):
        log(filename,"Le soleil est couche, la porte doit etre fermee")
        log(filename,'Ouverture poulailler : ' + str(ouverturePorte))
        log(filename,'Fermeture poulailler : ' + str(fermeturePorte))
        lastlogtime=str(ephem.Date(ephem.localtime(ephem.now())))
        log(filename,'Date actuelle        : ' + lastlogtime)
        log(filename,'Etat porte           : ' + str(etatPorte)) 
        closeDoor()
        log(filename,"Commande ouverture envoyee, attente fermeture")
        while(etatPorte == 'ouverte'):
          if (not GPIO.input(pinHallDoorLow)):
            emergencyBreakDoor()
            etatPorte = 'fermee'
            log(filename,"Porte Fermee")
            lastlogtime=str(ephem.Date(ephem.localtime(ephem.now())))
            log(filename,'Date actuelle        : ' + lastlogtime)
            log(filename,'Etat porte           : ' + str(etatPorte))
    if (ephem.Date(ephem.Date(lastlogtime)+ephem.hour) > ephem.Date(maintenant)):
      log(filename,"Hour Log")
      log(filename,'Ouverture poulailler : ' + str(ouverturePorte))
      log(filename,'Fermeture poulailler : ' + str(fermeturePorte))
      lastlogtime = str(ephem.Date(ephem.localtime(ephem.now())))
      log(filename,'Date actuelle        : ' + lastlogtime)
      log(filename,'Etat porte           : ' + str(etatPorte))      
    time.sleep(350)
except (KeyboardInterrupt, SystemExit):
  print "Arret du programme par Ctrl+c"
  log(filename,"Arret du programme par Ctrl+c")
  raise 
finally:
  log(filename,"Arret du programme")
  emergencyBreakDoor()
  GPIO.cleanup()
  #Quand on a fini toute l'application (si celle-ci a une fin), on efface le fichier disant que l'application est lancee
  # os.unlink(pidfile)
  print "Arret du programme..."
  raise 
