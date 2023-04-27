from network import LoRa
import socket
import time
import ubinascii
import binascii
import pycom
import struct
import math as m

from pysense import Pysense
from SI7006A20 import SI7006A20 
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE

py = Pysense()
si = SI7006A20(py)
mpPress = MPL3115A2(py,mode=PRESSURE)

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
app_eui = ubinascii.unhexlify('0000000000000019')
app_key = ubinascii.unhexlify('CAEAA1E267FF98C6B580413004DED61C')
dev_eui = ubinascii.unhexlify('0A02F5EF201A2102')

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

     temperature = int(si.temperature()*100)
     humidity = int(si.humidity()*100)
     pressure = int(mpPress.pressure()/10)
     contador = (contador + 1)

     print('Temperature:', temperature/100 )
     print('Humidity:', humidity/100)
     print('Pressure:', pressure/10)
     print('Numero de paquete', contador)

     data = bytearray(struct.pack('h',temperature)+struct.pack('h',humidity)+struct.pack('h',pressure)+struct.pack('h',contador))

     print('Sending data (uplink)...')

     # send some data
     s.send(data)

     # make the socket non-blocking
     # (because if there's no data received it will block forever...)
     s.setblocking(False)

     print('Data Sent: ', data)
     pycom.rgbled(0x00CC00) # green
     time.sleep(6)