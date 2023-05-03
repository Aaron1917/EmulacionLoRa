from network import LoRa
import os
import socket
import time
import utime
import ubinascii
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

# Deshabilitar el heartbeat LED
pycom.heartbeat(False)

# Inicializar LoRa en modo LORAWAN.
# Escogemos la region de nuestro dispositivo:
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# Creamos los parámetros de autentificación OTAA.
app_eui = ubinascii.unhexlify('000000000000000A')
app_key = ubinascii.unhexlify('CA62C2B68891D25D407ABB2812A27386')
dev_eui = ubinascii.unhexlify('70B3D57ED005BF1F')

# Removemos los canales 0-8 16-72.
for i in range(0,8):
     lora.remove_channel(i)
for i in range(16,65):
     lora.remove_channel(i)
for i in range(66,72):
     lora.remove_channel(i)

# Intemos la conexión usando OTAA (Over the Air Activation).
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# Esperamos hasta que el módulo se una a la red.
while not lora.has_joined():
    pycom.rgbled(0x0A0A08) # blanco.
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined LoRa network')
pycom.rgbled(0x00CC00) # verde

# Creamos un socket LoRa.
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Establecemos el LoRa Spreading Factor (SF) y bandwidth (BW)
# SF10BW125
# SF9BW125
# SF80BW125
# SF70BW125
# SF8BW500
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 1)
# s.setsockopt(socket.SOL_LORA, socket.SO_POWER, 14) # 14 dBm

contador = 0
data = ''
# data2 = ''
# start_time = utime.ticks_ms()

total_time = 1800 # 30m * 60s
total_msg = 15
tpm = int((total_time/total_msg)*1000)  # 120,000 ms 
# 30 min/15 msj

while True:
     # Calculamos un número aleatoreo entre 0 y el maximo en ms de tiempo
     # para enviar el mensaje descontando el sleep(1) y el tiempo de envio 6270ms
     wait = randint(0, tpm - 8000)
     print('Los ms son:')
     print(wait)
     utime.sleep_ms(wait)
     # make the socket blocking
     # (waits for the data to be sent and for the 2 receive windows to expire)
     s.setblocking(True)
     pycom.rgbled(0xFF3399) # rosa
     # Cronometreamos el tiempo 
     start_time = utime.ticks_ms()
     # envio de datos
     contador += 1
     print('Numero de paquete', contador)
     data = bytearray(struct.pack('h', contador))

     data2 = sensores()
     data += data2
     print('Sending data (uplink)...')
     # envio de datos
     s.send(data)
     # make the socket non-blocking
     # (because if there's no data received it will block forever...)
     s.setblocking(False)
     print('Data Sent: ', data)
     pycom.rgbled(0x00CC00) # verde
     # tomamos el tiempo en terminar el envio...
     end_time = utime.ticks_ms()
     exe_time = utime.ticks_diff(end_time, start_time)
     print('El tiempo de ejecucion: ')
     print(exe_time)
     # Tomamos el tiempo restante que es igual a:
     # Tiempo por mensaje - tiempo esperado al inicio -tiempo de ejecución - 1s
     time.sleep(1)
     if tpm-wait-exe_time > 0:
          utime.sleep_ms(tpm-wait-exe_time)
     #El tiempo total esperado debe ser de 120,000 ms
