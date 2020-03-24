import serial

ser = serial.Serial('COM3',baudrate=9600,timeout=1)

while True:
    ser.write(1)
