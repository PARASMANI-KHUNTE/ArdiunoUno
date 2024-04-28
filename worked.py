import serial
import time

# Adjust the COM port and baud rate accordingly
ser = serial.Serial('COM3', 9600, timeout=1)

def move_servo(command):
    # Send command to Arduino
    ser.write(command.encode())
    # Delay to allow Arduino to process the command
    time.sleep(0.1)

# Define movements
movements = {'L': 'left', 'R': 'right', 'U': 'up', 'D': 'down'}

# Main loop
while True:
    # Get movement command from user
    user_input = input("Enter movement command (L/R/U/D): ")
    if user_input in movements:
        # Send command to Arduino
        move_servo(user_input)
        print(f"Moving {movements[user_input]}")
    else:
        print("Invalid command. Please enter L, R, U, or D.")

# Close serial connection
ser.close()
