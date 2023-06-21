import socket

# Receiver IP and port
receiver_ip = "192.168.2.2"
receiver_port = 8888

# Create a socket object
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP and port
receiver_socket.bind((receiver_ip, receiver_port))

# Listen for incoming connections
receiver_socket.listen(1)
print("Listening for incoming connections.")

# Accept a connection from the sender
sender_socket, sender_address = receiver_socket.accept()
print("Connection Accepted.")

while True:
    # Receive data from the sender
    data = sender_socket.recv(1024).decode()

    if data:
        print("Message received:", data)

# Close the sender socket
sender_socket.close()

# Close the receiver socket
receiver_socket.close()