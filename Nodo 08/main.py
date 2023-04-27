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

# Se deshabilita el led que prende y apaga en azul
pycom.heartbeat(False)

# Se inicializa LoRa en el modo LoRaWAN y se selecciona la frecuencia
# correspondiente a Uruguay

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# create an OTAA authentication parameters, change them to the provided credentials

app_eui = ubinascii.unhexlify('0000000000000008')
dev_eui = ubinascii.unhexlify('114AA912F8BC882A')
app_key = ubinascii.unhexlify('57769376BB66E9B358F016A4DE5CBE74')

#Se eliminan los canales del 0 al 72
for i in range(0,8):
     lora.remove_channel(i)
for i in range(16,65):
     lora.remove_channel(i)
for i in range(66,72):
     lora.remove_channel(i)

# Se configura la conexión con la red OTA
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# Esperamos a que el nodo se una a la red
while not lora.has_joined():
    pycom.rgbled(0x0A0A08) # white
    time.sleep(2.5)
    print('Not yet joined...')

# El nodo se une a la red y se prende el led en verde

print('Joined LoRa network')
pycom.rgbled(0x00CC00) # green

# Se crea el socket LoRa
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Se configura la tasa de transmisión de datos de LoRa

s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)

# Se inicializa la variable contador que cuenta la cantidad de paquetes enviados

contador = 0

#Inicia un loop en el que se envía información cada un tiempo determinado

while True:

    # se configura el socket para que se bloquee (que espere que se mande la información
     # y luego las dos ventanas de recepción - Clase A)
     
     s.setblocking(True)

     # se prende el led en rosa indicando que se está enviando la información
     
     pycom.rgbled(0xFF3399) #pink

     #se guarda en las variables temperature, humidity y pressure las coordenadas obtenidas por el nodo
     
     temperature = int(si.temperature()*100)
     humidity = int(si.humidity()*100)
     pressure = int(mpPress.pressure()/10)

     #el contador suma un paquete
     
     contador = (contador + 1)

     print('Temperature:', temperature/100 )
     print('Humidity:', humidity/100)
     print('Pressure:', pressure/10)
     print('Numero de paquete', contador)

     # se guardan las variables temperature, humidity, pressure y contador en una variable data como un bytearray
     data = bytearray(struct.pack('h',temperature)+struct.pack('h',humidity)+struct.pack('h',pressure)+struct.pack('h',contador))

     print('Sending data (uplink)...')

     # envía la información
     s.send(data)

     # desbloquea el socket
     s.setblocking(False)

     print('Data Sent: ', data)

     # Entra en modo sleep por 20 segundos y el led se pone en verde, luego vuelve a comenzar el loop
     
     pycom.rgbled(0x00CC00) # green
     time.sleep(6)

