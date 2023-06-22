import socket
import time

# Function to connect to the socket and accept incoming connections
def socket_connect(receiver_sock):
    sender_socket = None
    try:
        # Listen for incoming connections
        receiver_sock.listen(1)
        print("Listening for incoming connections.")

        # Accept a connection from the sender
        sender_socket, sender_address = receiver_sock.accept()
        print(f"Connection accepted from {sender_address}.")
        
    except socket.timeout:
        print("Connection timed out.")
        
    return sender_socket

# Function to check socket activity
def check_socket_activity(sock):
    try:
        sock.settimeout(5)
        # Attempt to receive data from the socket
        data = sock.recv(1024).decode()
        if data:
            return True  # Data received
        else:
            return False  # No data received
    except socket.timeout:
        return False  # Socket timed out

receiver_ip = "192.168.2.2"
receiver_port = 8888

# Create a socket object
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP and port
try:
    receiver_socket.bind((receiver_ip, receiver_port))
    print(f"Socket successfully bound to address: ({receiver_ip}, {receiver_port})")
except OSError:
    print("OSError occurred. Please check your network settings.")
    exit()

# Accept connection
sender_socket = socket_connect(receiver_socket)

while True:
    if sender_socket:
        # Receive data from the sender
        data = sender_socket.recv(1024).decode()

        if data:
            print("Message received:", data)
        else:
            print("Error: No data received. Checking if socket is still receiving data.")

            if not check_socket_activity(receiver_socket):
                print("Socket is no longer active.")

                # Retry connection after a delay
                for i in range(5, 0, -1):
                    print(f"Retrying connection in {i} seconds.")
                    time.sleep(1)

                sender_socket = socket_connect(receiver_socket)
    else:
        print("Error: No connection established. Retrying in 5 seconds.")

        # Retry connection after a delay
        for i in range(5, 0, -1):
            print(f"Retrying connection in {i} seconds.")
            time.sleep(1)

        sender_socket = socket_connect(receiver_socket)

# Close the sender socket
sender_socket.close()

# Close the receiver socket
receiver_socket.close()