import serial
import time

# Default port specified for Raspberry Pi 4, port should be filled on Windows or Linux
def init_serial(port='/dev/ttyACM0', baud_rate=9600):
    ser = serial.Serial(port, baud_rate)
    time.sleep(2)  # Ensure the connection is established
    return ser

def send_message(ser, message):
    ser.write((message + '\n').encode())

def receive_message(ser):
    if ser.in_waiting > 0:
        return ser.readline().decode('utf-8').rstrip()
    return None

def close_serial(ser):
    ser.close()

################################################## PROOF OF CONCEPT DEBUG CODE ##################################################

# # Set up the serial connection (the port name will vary, so check it)
# ser = serial.Serial('/dev/ttyACM0', 9600)

# # Ensure the connection is established
# time.sleep(2)

# try:
#     while True:
#         # Send a message to the Arduino
#         ser.write('Hello from Raspberry Pi!\n'.encode())

#         # Read and print the Arduino's response
#         if ser.in_waiting > 0:
#             line = ser.readline().decode('utf-8').rstrip()
#             print(line)

#         time.sleep(2)

# except KeyboardInterrupt:
#     print("Program terminated!")

# finally:
#     ser.close()  # Close the serial connection
    
    
##############################################################################################################################