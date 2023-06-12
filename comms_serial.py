import serial

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
                    timeout = 5 #wait 5 seconds before returning recieved bytes
                    )


# Read and parse data from the serial port
while True:
    if ser.in_waiting > 0: #data in buffer?
        data = ser.readline().decode() #decode removes any characters before and after data packet
        attitude_data = parse_attitude_data(data)
        if attitude_data is not None:
            yaw_att, roll_att, pitch_att = attitude_data
            print("yaw: " + str(yaw_att) + ", pitch: " + str(pitch_att) + ", roll: " + str(roll_att))

#close port.
ser.close()