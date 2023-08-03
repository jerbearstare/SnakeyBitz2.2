
import serial
import time

#Define Channel
Serial_channel = serial.Serial('COM3',9600) 
time.sleep(2) 

# open channel with arduino
while True:
    b = Serial_channel.readline()
    raw =  b.decode() # convert to string
    ardBank =  raw.rstrip()  # strip away excess characters
    print(ardBank)

#close Serial channel
Serial_channel.close() 