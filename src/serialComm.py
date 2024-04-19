import serial
import time

# Set up the serial connection (the port name will vary, so check it)
ser = serial.Serial('/dev/ttyACM0', 9600)

# Ensure the connection is established
time.sleep(2)

try:
    while True:
        # Send a message to the Arduino
        ser.write('Hello from Raspberry Pi!\n'.encode())

        # Read and print the Arduino's response
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)

        time.sleep(2)

except KeyboardInterrupt:
    print("Program terminated!")

finally:
    ser.close()  # Close the serial connection