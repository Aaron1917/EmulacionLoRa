# EmulacionLoRa
## Descripción General
Este proyecto pretende emular diferentes nodos LoRa en una red con dispositivos LoPy4 y FiPy en Montevideo, Uruguay. Para la red que se utilizó es mediante el LoRaWAN Gateway UG67 Milesight, y con el servidor de The Things Network (TTN). De acuerdo a los parámetros regionales de del US915 LoRa WAN 1.0.2 de determinaron parte de las condiciones del experimeto asi como la selección de la Sub Banda de trabajo 2 (FSB2).
## Condiciones del experimento  
 Las condiciones para las que se presenta dicha emulación sera bajo los siguientes parámetros:
 * El dispositivo en condiciones normales envia un payload de 8 bytes cada 30 minutos.
 * Spreding Factor (SF) = 9
 * Band Width (BW) = 125kHz
 * Code Rate (CR) = 1 (4/5)
 * El (Time of Airtime) ToA estimado es de 205.82 ms 
 Para dicha emulación se cuentan con 32 dispositivos físicos y se pretende emular diferentes cantidades:
 
 - 500 nodos
 - 1000 nodos
 - 1500 nodos
 - 2000 nodos
 
En esta segunda parte unicamente se aborda el contenido para **32** dispositivos que trabajan bajo las condiciones anteriormente especificadas y que para este tercer caso pretende emular **1500** nodos por lo tanto la carga de cada dispositivo a enviar es de **47** paquetes cada 30 minuto. Dejando un pequeño porcentaje extra para compensar la pérdida de tiempo en el procesamiento de cada nodo.


# Fase 2
Se desea conocer un caso mas experimental con **25** dispositivos que emulen **525**  y manden **12bytes/hora** por lo tanto tendremos que cada dispositivo fisico emula **21** dispositivos. Ademas 7 o **5** dispositivos fisicos emularan el envio de **1.2kbytes/hora**.
## Condiciones 2
 Las condiciones para las que se presenta dicha emulación sera bajo los siguientes parámetros para los primeros 25 dispositivos fisicos del nodo **1** al nodo **25**:
 * Band Width (BW) = 125kHz
 * Code Rate (CR) = 1 (4/5)
 * PHY Payload = 28 a 29 bytes

 | Spreding Factor (SF) | Time of Airtime (ToA) |
 |;---;|;---;|
 | 9 | 226.3 ms |
 | 8 |123.39 ms |
 | 7 | 66.81 ms |

Los dispositivos que emularan **1.2kbytes/hora**, del nodo **26** al nodo **34** tendran:
(se puede subdivdir en 200bytes/10min )
 * Band Width (BW) = 125kHz
 * Code Rate (CR) = 1 (4/5)
 * PHY Payload = 216-217 bytes

 | Spreding Factor (SF) | Time of Airtime (ToA) |
 |;---;|;---;|
 | 7 | 343.29 ms |
