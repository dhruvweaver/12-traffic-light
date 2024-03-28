#hardware connection: 
#Connect the UART TX pin of the Raspberry Pi to FPGA'S UART RX pin
#Connect the UART RX pin of the Raspberry Pi to the FPGA's UART TX pin
#Make sure to connect GND Of both device

import serial
import time
#import subprocess
#import os

#configure the serial port
ser = serial.Serial("/dev/ttyS0", 9600)

while True:
    #give permissions to write
    #subprocess.run("sudo chmod 666 /dev/ttyS0", shell=True)
    
    #send data to FPGA
    #speed = 250
    #braking = "B"
    #sendData = f"{braking} {speed}\r\n"
    sendData = "test\r\n"
    ser.write(bytes(sendData,'utf-8'))
    print(f"Sent: {sendData}")
  
    #add delay
    time.sleep(1)
