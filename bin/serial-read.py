import serial

if __name__ == '__main__':
    Serial_channel = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    Serial_channel.flush()

    while True:
        if Serial_channel.in_waiting > 0:
            b = Serial_channel.readline()
            raw =  b.decode() # convert to string
            ardBank =  raw.rstrip('utf-8')# strip away excess characters
            print(ardBank)