from network import LoRa
import socket
import time
import ubinascii
import binascii
import pycom
import struct
import machine
import math
import network
import os
import utime
import gc
from machine import RTC
from machine import SD
from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12
from pycoproc_1 import Pycoproc

py = Pycoproc (Pycoproc.PYTRACK)
l76 = L76GNSS(py, timeout=30)
li = LIS2HH12(py)

# Disable heartbeat LED
pycom.heartbeat(False)

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('0000000000000002')
app_key = ubinascii.unhexlify('4108AB63B41861777ADAC0CCF5F80612')
dev_eui = ubinascii.unhexlify('02EFADC984153AFA')

#Uncomment for US915 / AU915 & Pygate
for i in range(0,8):
     lora.remove_channel(i)
for i in range(16,65):
     lora.remove_channel(i)
for i in range(66,72):
     lora.remove_channel(i)

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    pycom.rgbled(0x0A0A08) # white
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined LoRa network')
pycom.rgbled(0x00CC00) # green


# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)
contador = 0

while True:

     # make the socket blocking
     # (waits for the data to be sent and for the 2 receive windows to expire)
     s.setblocking(True)

     pycom.rgbled(0xFF3399) #pink
    
     #f.write("{} - {}\n".format(coord, rtc.now()))
     coord = l76.coordinates()
     contador = (contador + 1)

     print('Coordenadas:', coord )
     print('Numero de paquetes', contador )

     if coord[0] != None:
        lat = int(coord[0]*(-100))
        long = int(coord[1]*(-100))
        acc = int(li.acceleration()[2]*100)

        print (lat)
        print (long)
        print("Acceleration: " + str(acc/100))

        data = bytearray(struct.pack('h',lat)+struct.pack('h',long)+struct.pack('h', acc)+struct.pack('h',contador))

        print('Sending data (uplink)...')

        # send some data
        s.send(data)

        # make the socket non-blocking
        # (because if there's no data received it will block forever...)
        s.setblocking(False)

        print('Data Sent: ', data)
     else:
        nolat = 00
        nolong = 00

        acc = int(li.acceleration()[2]*100)
        rol = int(li.roll()*100)
        pit = int(li.pitch()*100)

        print("Acceleration: " + str(acc/100))
        print("Roll: " + str(rol/100))
        print("Pitch: " + str(pit/100))

        data = bytearray(struct.pack('h', rol)+struct.pack('h', pit)+struct.pack('h', acc)+struct.pack('h',contador))

        print('Sending data (uplink)...')

        # send some data
        s.send(data)

        # make the socket non-blocking
        # (because if there's no data received it will block forever...)
        s.setblocking(False)

        print('Data Sent: ', data)
        
     pycom.rgbled(0x00CC00) # green
     time.sleep(6)