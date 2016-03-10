#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#  
#       Hall Effect Sensor
#
# This script tests the sensor on GPIO17.
#
# Author : Matt Hawkins
# Date   : 27/09/2015
#
# http://www.raspberrypi-spy.co.uk/
#
#-------------------------------------- 

# Import required libraries
import RPi.GPIO as GPIO
import time
import datetime

# Tell GPIO library to use GPIO references
GPIO.setmode(GPIO.BCM)

print "Setup GPIO pin as input"
pinput=18
# Set Switch GPIO as input
GPIO.setup(pinput , GPIO.IN, pull_up_down = GPIO.PUD_UP)

def sensorCallback1(channel):
  # Called if sensor output goes LOW
  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
  print "Sensor LOW " + stamp

def sensorCallback2(channel):
  # Called if sensor output goes HIGH
  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
  print "Sensor HIGH " + stamp
  
def main():
  # Wrap main content in a try block so we can
  # catch the user pressing CTRL-C and run the
  # GPIO cleanup function. This will also prevent
  # the user seeing lots of unnecessary error
  # messages.
  
  GPIO.add_event_detect(pinput, GPIO.FALLING, callback=sensorCallback1, bouncetime = 500)  
  GPIO.add_event_detect(pinput, GPIO.RISING, callback=sensorCallback2, bouncetime = 500) 
  
  try:
    # Loop until users quits with CTRL-C
    while True :
      time.sleep(0.1)
        
  except KeyboardInterrupt:
    # Reset GPIO settings
    GPIO.cleanup()
  
if __name__=="__main__":
   main()
