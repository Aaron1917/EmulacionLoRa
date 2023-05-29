from network import LoRa
import os
import socket
import time
import utime
import ubinascii
import binascii
import pycom
import struct

from pysense import Pysense
from SI7006A20 import SI7006A20 
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE

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
     temperature = int(si.temperature()*100)
     humidity = int(si.humidity()*100)
     pressure = int(mpPress.pressure()/10)
     print('Temperature:', temperature/100 )
     print('Humidity:', humidity/100)
     print('Pressure:', pressure/10)
     data = bytearray(struct.pack('h',temperature)+struct.pack('h',humidity)+struct.pack('h',pressure))
     return data

py = Pysense()
si = SI7006A20(py)
mpPress = MPL3115A2(py,mode=PRESSURE)

pycom.heartbeat(False)

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

app_eui = ubinascii.unhexlify('0000000000000018')
app_key = ubinascii.unhexlify('51123F3FF201EFFD361DE7D640AD62E6')
dev_eui = ubinascii.unhexlify('0A02F5A1E0DB1556')

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

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 1)

contador = 0
data = ''

total_time = 1800 # 30m * 60s
total_msg = 15 # 15 mensajes
tpm = int((total_time/total_msg)*1000)  # 120,000 ms 
# 30 min/15 msj

while True:
     wait = randint(0, tpm - 8000)
     # print('Los ms son:')
     # print(wait)
     utime.sleep_ms(wait)

     s.setblocking(True)
     pycom.rgbled(0xFF3399)
     start_time = utime.ticks_ms()
     contador += 1
     print('Numero de paquete', contador)
     data = bytearray(struct.pack('h', contador))

     data2 = sensores()
     data += data2
     print('Sending data (uplink)...')

     s.send(data)
     s.setblocking(False)
     print('Data Sent: ', data)
     pycom.rgbled(0x00CC00) 

     end_time = utime.ticks_ms()
     exe_time = utime.ticks_diff(end_time, start_time)
     print('El tiempo de ejecucion: ')
     print(exe_time)

     time.sleep(1)
     if tpm-wait-exe_time > 0:
          utime.sleep_ms(tpm-wait-exe_time)
