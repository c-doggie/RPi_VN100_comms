# RPi to VN100 IMU Sensor
This is a basic script that enables the Raspberry Pi to communicate with a VectorNav VN100 sensor via the Serial UART port. It uses the PySerial library and Socket library. 

It features basic TCP networking code to send the packet to a base station receiver who is awaiting the sensor readings. This code is now deprecated due to my switching from hand-crafted TCP networking to ROS 2-based networking.

Here's a wiring diagram:

![On VN100: GND to 5,VCC to 1, RX to 9, TX to 8. On RPI: VCC to 1, GND to 6, RX(Pi) to 8, TX(Pi) to 10](/img/RPi_VN100_diagram.jpg "Raspberry Pi to VN100 UART Wiring Diagram.")

Note: this script assumes that the VN100 is using the factory configuration of what the sensor outputs by default. It will not work with a custom configuration.
