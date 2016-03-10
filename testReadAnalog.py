
import RPi.GPIO as GPIO  
from time import sleep     # this lets us have a time delay (see line 12)  
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
pinHall1=2
#GPIO.setup(pinHall1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set GPIO25 as input (hall1)  
GPIO.setup(pinHall1, GPIO.IN)    # set GPIO25 as input (hall1)  
#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set GPIO24 as input (hall2)  
  

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

try:  
    while True:            # this will carry on until you hit CTRL+C  
		GPIO.add_event_detect(pinHall1, GPIO.BOTH, callback=sensorCallback1)  
		#GPIO.add_event_detect(pinHall1, GPIO.RISING, callback=sensorCallback2)
		sleep(0.1)         # wait 0.1 seconds
        #if GPIO.input(pinHall1): # if port 25 == 1  
        #print "Port 2piHall1 is 1/HIGH/True - LED ON"  
        #GPIO.output(24, 1)         # set port/pin value to 1/HIGH/True  
        #else:  
        #print "Port pinHall1 is 0/LOW/False - LED OFF"  
        #GPIO.output(24, 0)         # set port/pin value to 0/LOW/False  
  
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup() 
