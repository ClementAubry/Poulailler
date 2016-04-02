import signal
import sys

def signal_handler(signum, frame):
  raise Exception("Timed out Exception!")

timeoutDoorActuator=4

signal.signal(signal.SIGALRM, signal_handler)
signal.alarm(timeoutDoorActuator)   # Ten seconds
try:
  while True:
    pass
except Exception as err:
  print(err)
