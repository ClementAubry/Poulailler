
import signal
from serial import *
from threading import Thread
from time import *

last_received = ''

def receiving(ser):
    global last_received
    buffer = ''

    while True:
        # last_received = ser.readline()
        buffer += ser.read(ser.inWaiting())
        if '\n' in buffer:
            last_received, buffer = buffer.split('\n')[-2:]


if __name__ ==  '__main__':
    ser = Serial(
        port='/dev/arduino',
        baudrate=9600,
        bytesize=EIGHTBITS,
        parity=PARITY_NONE,
        stopbits=STOPBITS_ONE,
        timeout=0.1,
        xonxoff=0,
        rtscts=0,
        interCharTimeout=None
    )
    try:
        threadSerial = Thread(target=receiving, args=(ser,))
        threadSerial.setDaemon(True)
        threadSerial.start()
        filename = 'lightSensor' + strftime("%Y%m%d-%H%M%S") + '.txt'
        print(filename)
        # sys.stdout = open(filename, 'w')
        while True:
          timestr = strftime("%d/%m/%Y %H:%M:%S UTC")
          if (last_received):
            strdata = timestr + ' ' + last_received
            print(strdata)
            f = open(filename, 'a')
            f.write(strdata)
            f.close()
          # print(strdata, filename)
          sleep(350) #Sleep in seconds (350=5min)
    except (KeyboardInterrupt, SystemExit):
        print('You pressed Ctrl+C!')
        # cleanup_stop_thread();
        sys.exit()
