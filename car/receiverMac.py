import serial

# Configure the serial port
ser = serial.Serial('/dev/tty.usbserial-0001', 9600)  # Use the correct device name

while True:
    # Receiving data
    received_data = ser.readline().decode('utf-8').strip()
    if received_data:
        print(f"Received: {received_data}")
