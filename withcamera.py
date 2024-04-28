import cv2
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

# Initialize camera
cap = cv2.VideoCapture(0)

# Define color range for object tracking (in HSV format)
lower_blue = (100, 50, 50)
upper_blue = (140, 255, 255)

# Main loop
while True:
    # Read frame from camera
    ret, frame = cap.read()
    
    # Convert frame from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # If contours are found
    if contours:
        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get the centroid of the largest contour
        M = cv2.moments(largest_contour)
        
        # Check if area of contour is non-zero to avoid division by zero
        if M["m00"] != 0:
            centroid_x = int(M["m10"] / M["m00"])
            centroid_y = int(M["m01"] / M["m00"])
            
            # Determine movement direction based on centroid position
            if centroid_x < frame.shape[1] // 3:
                movement = 'L'
            elif centroid_x > 2 * frame.shape[1] // 3:
                movement = 'R'
            elif centroid_y < frame.shape[0] // 3:
                movement = 'U'
            elif centroid_y > 2 * frame.shape[0] // 3:
                movement = 'D'
            else:
                movement = None
        
            # If a valid movement direction is detected, send the corresponding command to Arduino
            if movement:
                move_servo(movement)
                print(f"Moving {movements[movement]}")
    
    # Display the frame
    cv2.imshow('Frame', frame)
    
    # Check for keyboard input
    key = cv2.waitKey(1)
    
    # If 'q' is pressed, exit the loop
    if key == ord('q'):
        break

# Release camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Close serial connection
ser.close()
