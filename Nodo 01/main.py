from network import LoRa
import os
import socket
import time
import utime
import ubinascii
import binascii
import pycom
import struct

from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12
from pycoproc_1 import Pycoproc

# La siguiente funcion crea un numero entero de 4 bytes de manera 'aleatorea'
# El número puede estar contenido dentro de un rango especificado (4294967295)
def randint(min = 0, max = 2147483647):
    val = 0
    while (val == 0):
        val = struct.unpack('I', os.urandom(4))[0]
    num = val % (max - min)
    return int(num + min)


def sensores():
     coord = l76.coordinates()
     # print('Coordenadas:', coord )
     # print('Numero de paquetes', contador )
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

# Inicializar LoRa en modo LORAWAN.
# Escogemos la region de nuestro dispositivo:
# lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# Creamos los parámetros de autentificación OTAA.
app_eui = ubinascii.unhexlify('0000000000000001')
app_key = ubinascii.unhexlify('681D46C8E62613E607CBEAA5617064A5')
dev_eui = ubinascii.unhexlify('0898FDA25920BCD5')

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
# DR0     SF10BW125
# DR1     SF9BW125
# DR2     SF80BW125
# DR3     SF70BW125
# DR4     SF8BW500
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)

contador = 0
data = ''

total_time = 3600 # 60m * 60s
total_msg = 21
# Tiempo por mensaje 
tpm = int((total_time/total_msg)*1000)

while True:
     # Calculamos un número aleatoreo entre 0 y el maximo en ms de tiempo
     # para enviar el mensaje descontando el sleep(1) y el tiempo de envio 6270ms
     wait = randint(0, tpm - 8000)
     print('Los ms son:')
     print(wait)
     utime.sleep_ms(wait)
     pycom.rgbled(0xFF3399) # rosa
     # Cronometreamos el tiempo 
     start_time = utime.ticks_ms()
     # envio de datos
     contador += 1
     print('Numero de paquete', contador)
     data = bytearray(struct.pack('h', contador)) # B
     data2 = sensores() + bytearray(os.urandom(4))
     data += data2
     # Se bloquea el socket 
     # (Se espera a que se envien los datos y que caduquen las 2 ventanas de recepción)
     s.setblocking(True)
     print('Sending data (uplink)...')
     # envio de datos
     s.send(data)
     # Se desactiva el bloqueo del socket
     # (Si no se desactiva se puede bloquear para siempre...)
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
          utime.sleep_ms(tpm-wait-exe_time-1000)
