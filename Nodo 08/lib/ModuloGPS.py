import time
import pycom
from pytrack import Pytrack
from LIS2HH12 import LIS2HH12
from L76GNSS import L76GNSS


py = Pytrack()
li = LIS2HH12(py)

# after 60 seconds of waiting without a GPS fix it will
# return None, None
gnss = L76GNSS(py, timeout=60)

# Disable heartbeat LED
pycom.heartbeat(False)

while True:
    pycom.rgbled(0x000014)

    print('\n\n** GPS (L76GNSS)')
    loc = gnss.coordinates()        #espera un minuto por las cordenadas
    
    if loc[0] == None or loc[1] == None:
        print('No GPS fix within configured timeout :-(')
    else:
        print('Latitude', loc[0])
        print('Longitude', loc[1])
    pycom.rgbled(0x001400)
    time.sleep(10)
