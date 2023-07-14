import serial
import time

ser = serial.Serial(port='/dev/serial0',
                    baudrate=115200,
                    timeout=None  # Wait indefinitely for data.
                    )

timestamps = []  # List to store message timestamps


try:
    while True:
        # Read data from the serial port
        data = ser.readline()
        
        # Process the received data
        if data:
            # Calculate delta_t between messages
            current_time = time.time()
            timestamps.append(current_time)
            
            # Do something with the received data
            print("Received: " + data.decode().strip())
            
except KeyboardInterrupt:
    # Program exits on KeyboardInterrupt (e.g., Ctrl+C)
    if timestamps:
        # Calculate average delta_t
        delta_ts = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
        average_delta_t = sum(delta_ts) / len(delta_ts)
        print("Average delta_t:", average_delta_t)
    else:
        print("No messages received.")

finally:
    ser.close()
