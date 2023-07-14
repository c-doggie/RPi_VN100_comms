import socket
import serial
import time
from sys import exit

# Sender IP and port
#sender_ip = "192.168.2.3" # RPi IP if on Belkin Router --> Check router settings for this IP.
sender_ip = "169.254.48.2" # RPi IP if on LabSwitch Eth Connection. --> Check wired internet settings for this IP.
sender_port = 8888

# Receiver IP and port
#receiver_ip = "192.168.2.2" # NUC IP if on Belkin Router --> Check router settings for this IP.
receiver_ip = "169.254.48.36" # NUC IP if on LabSwitch Eth Connection. --> Check wired internet settings for this IP.
receiver_port = 8888

start_time = time.time_ns()

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
    data = data[:-5].strip() #I have zero clue why it's -5. I think the ascii output of the sensor maybe puts whitespaces after the message? It should be -3 to accocunt for the lat 3 characters.
    values = data.split(",")

    if len(values) >= 4 and values[0] == "$VNYPR":
        yaw_att = float(values[1].strip())
        pitch_att = float(values[2].strip())
        roll_att  = float(values[3].strip())
        return yaw_att, pitch_att, roll_att
    return None


# Create a serial port object
ser = serial.Serial(port = '/dev/serial0', 
                    baudrate=115200,
                    timeout = None #Wait indefinitely for data.
                    )


print("Serial port initialized, waiting for data...")
time.sleep(3)


# Read and parse data from the serial port
avg_delta_t = 0.0
sum_delta_t = 0.0
current_time = 0
count = 0

while True:
    if ser.in_waiting > 0: #data in buffer?
        data = ser.readline().decode() #decode removes any characters before and after data packet
        attitude_data = parse_attitude_data(data) #attitude is a tuple of 3 floats.
        
        if attitude_data is not None:
            try:
                #Delta T Calculation Code
                count += 1
                current_time = time.time_ns()
                delta_t = current_time - start_time
                sum_delta_t += delta_t

                yaw_att, pitch_att, roll_att = attitude_data
                print("yaw: " + str(yaw_att) + ", pitch: " + str(pitch_att) + ", roll: " + str(roll_att) + ", delta_t: " + str(delta_t))
                
                start_time = current_time

                #send attitude data to ground station.
                sender_socket.send(str(attitude_data).encode())

            except BrokenPipeError:
                print("Some error occured with the receiver connection. Exiting Script.")

                avg_delta_t = sum_delta_t / count
                print("Average delta_t: " + str(avg_delta_t / 10**6) + "ms")
                exit()
#close port.
ser.close()
sender_socket.close()