#hardware connection: 
#Connect the UART TX pin of the Raspberry Pi to FPGA'S UART RX pin
#Connect the UART RX pin of the Raspberry Pi to the FPGA's UART TX pin
#Make sure to connect GND Of both device

import serial
import time

#configure the serial port
ser = serial.Serial("/dev/cu.usbserial", 9600)

while True:
    #send data to FPGA
    sendData = "Hi, FPGA!"
    ser.write(sendData.encode('utf-8'))
    print(f"Sent: {sendData}")

    #receving data from FPGA
    recivedData = ser.readline().decode('utf-8').strip()
    if recivedData:
        print(f"Recived: {recivedData}")
    
    #add delay
    time.sleep(1)
