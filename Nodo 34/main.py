from network import LoRa
import os
import socket
import time
import utime
import ubinascii
import pycom
import struct

from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12
from pycoproc_1 import Pycoproc

# La siguiente funcion crea un numero entero de 4 bytes de manera 'aleatorea'
# El número puede estar contenido dentro de un rango especificado (4294967295)
def randint(min = 0, max = 2147483647):
    diff = max - min
    val = 0
    while (val == 0):
        val = struct.unpack('I', os.urandom(4))[0]
    num = val % diff
    return int(num + min)


def sensores():
     coord = l76.coordinates()
     if coord[0] != None:
        lat = int(coord[0]*(-100))
        long = int(coord[1]*(-100))
        flag = 2

        print (lat)
        print (long)
        print("Flag")

        data = bytearray(struct.pack('h',lat)+struct.pack('h',long)+struct.pack('h', flag))
     else:
        acc = int(li.acceleration()[2]*100)
        rol = int(li.roll()*100)
        pit = int(li.pitch()*100)

        print("Acceleration: " + str(acc/100))
        print("Roll: " + str(rol/100))
        print("Pitch: " + str(pit/100))

        data = bytearray(struct.pack('h', rol)+struct.pack('h', pit)+struct.pack('h', acc))
     return data


py = Pycoproc (Pycoproc.PYTRACK)
l76 = L76GNSS(py, timeout=30)
li = LIS2HH12(py)

# Deshabilitar el heartbeat LED
pycom.heartbeat(False)

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

app_eui = ubinascii.unhexlify('0000000000000022')
app_key = ubinascii.unhexlify('7117C4B5547D58EC88E9E5C2F1AB996A')
dev_eui = ubinascii.unhexlify('4E1520320DF56D5F')

for i in range(0,8):
     lora.remove_channel(i)
for i in range(16,65):
     lora.remove_channel(i)
for i in range(66,72):
     lora.remove_channel(i)

lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

while not lora.has_joined():
    pycom.rgbled(0x0A0A08)
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined LoRa network')
pycom.rgbled(0x00CC00)

# Creamos un socket LoRa.
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)

contador = 0
data = ''

total_time = 3600 # 60m * 60s
total_msg = 6
tpm = int((total_time/total_msg)*1000)

while True:
     wait = randint(0, tpm - 8000)
     utime.sleep_ms(wait)
     pycom.rgbled(0xFF3399)
     start_time = utime.ticks_ms()

     contador += 1
     print('Numero de paquete', contador)
     data = bytearray(struct.pack('h', contador))
     data2 = sensores() + bytearray(os.urandom(192))
     data += data2

     s.setblocking(True)
     print('Sending data (uplink)...')
     # envio de datos
     s.send(data)

     s.setblocking(False)
     print('Data Sent: ', data)
     pycom.rgbled(0x00CC00)
     end_time = utime.ticks_ms()
     exe_time = utime.ticks_diff(end_time, start_time)

     time.sleep(1)
     if tpm-wait-exe_time > 0:
          utime.sleep_ms(tpm-wait-exe_time)
