import serial
import time

def parse(str):
    if str[0] == 'B':
        print('braking')
    if str[0] == 'A':
        print('not braking')

    speed = float(str[2:8])
    print(f'speed: {speed} mph')

ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1,xonxoff=False)
while True:
    resp = ser.readline().decode("utf-8").strip()
    print(f"Received: {resp}")
    parse(resp)
