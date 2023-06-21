import socket
import time

# Sender IP and port
sender_ip = "192.168.2.2"
sender_port = 8888

# Receiver IP and port
receiver_ip = "192.168.2.3"
receiver_port = 8888

# Create a socket object
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the receiver
sender_socket.connect((receiver_ip, receiver_port))

while True:
    message = "Hello, receiver!"

    # Send the message to the receiver
    sender_socket.send(message.encode())

    # Wait for 1 second
    time.sleep(1)

# Close the socket
sender_socket.close()