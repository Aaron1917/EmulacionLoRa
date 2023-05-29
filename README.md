# EmulacionLoRa
## Descripción General
Este proyecto pretende emular diferentes nodos LoRa en una red con dispositivos LoPy4 y FiPy en Montevideo, Uruguay. Para la red que se utilizó es mediante el LoRaWAN Gateway UG67 Milesight, y con el servidor de The Things Network (TTN). Deacuardo a los parametros regionales de del US915 LoRa WAN 1.0.2 de determinaron parte de las condiciones del experimeto asi como la seleccion de la Sub Banda de trabajo (FSB2).
## Condiciones del experimento  
 Las condiciones para las que se presenta dicha emulacion sera bajo los siguientes parámetros:
 El dispositivo en condiciones normales envia un payload de 8 bytes cada 30 minutos.
 Spreding Factor (SF) = 9
 Band Width (BW) = 125kHz
 Code Rate (CR) = 1 (4/5)
 El (Time of Airtime) ToA estimado es de 205.82 ms 
 Para dicha emulación se cuentan con 32 dispositivos físicos y se pretende emular diferentes cantidades:
 
 - 500 nodos
 - 1000 nodos
 - 1500 nodos
 - 2000 nodos
En esta primera parte unicamente se aborda el contenido para 32 dispositivos que trabajan bajo las condiciones anteriormente especificadas y que para este primer caso pretende emular 500 nodos.
