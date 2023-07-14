import socket
import serial
import time
from sys import exit

# Sender IP and port
#sender_ip = "192.168.2.3" # RPi IP if on Belkin Router --> Check router settings for this IP.
sender_ip = "69.254.48.2" # RPi IP if on LabSwitch Eth Connection. --> Check wired internet settings for this IP.
sender_port = 8888

# Receiver IP and port
#receiver_ip = "192.168.2.2" # NUC IP if on Belkin Router --> Check router settings for this IP.
receiver_ip = "169.254.48.36" # NUC IP if on LabSwitch Eth Connection. --> Check wired internet settings for this IP.
receiver_port = 8888

# Create a socket object...
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try: 
    sender_socket.connect((receiver_ip, receiver_port))
    print("Connection to Receiver accepted.")
except ConnectionRefusedError: #connection denied.
    print("Connection to Receiver Denied. Try checking if the receiver script is running. \nExiting script.")
    sender_socket.close()
    exit()


def parse_attitude_data(data):
    # Example input: "$VNYMR, [yaw_float], [roll_float], [pitch_float],  ..."
    # Remove leading and trailing whitespaces
    data = data.strip()
    
    # Split the string using comma as the delimiter
    values = data.split(',')

    if len(values) >= 4 and values[0] == "$VNYMR":
        # Extract the yaw, roll, and pitch values
        yaw_att = float(values[1].strip())
        roll_att = float(values[3].strip())
        pitch_att = float(values[2].strip())
        return yaw_att, roll_att, pitch_att

    # Return None if the format doesn't match
    return None

# Create a serial port object
ser = serial.Serial(port = '/dev/serial0', 
                    baudrate=115200,
                    timeout = None #Wait indefinitely for data.
                    )


print("Serial port initialized, waiting for data...")
time.sleep(3)


# Read and parse data from the serial port

while True:
    if ser.in_waiting > 0: #data in buffer?
        data = ser.readline().decode() #decode removes any characters before and after data packet
        attitude_data = parse_attitude_data(data) #attitude is a tuple of 3 floats.
        if attitude_data is not None:
            yaw_att, roll_att, pitch_att = attitude_data
            print("yaw: " + str(yaw_att) + ", pitch: " + str(pitch_att) + ", roll: " + str(roll_att))
            #send attitude data to ground station.
            sender_socket.send(str(attitude_data).encode())

#close port.
ser.close()
sender_socket.close()