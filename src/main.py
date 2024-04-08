import cv2
import numpy as np
import time

from PIL import Image

from util import get_hsv_limits

cap = cv2.VideoCapture(0) # Webcam, needs to be changed from PC to laptop
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Camera is not available")
    exit()
else:
    print("Camera found in currently selected slot!")
    
start_time = time.time()
while True:
    print(time.time())
    if time.time() - start_time > 8:
        print("Error: No camera found within 8 seconds")
        cap.release()
        cv2.destroyAllWindows()
        exit()
    
    ret, frame = cap.read()
    if ret:
        print("Frame found!")
        break  # Exit the while loop if the frame is read successfully

# Test program to identify singular pixel color using only hue value

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)

    # Pick pixel value
    pixel_center = hsv_frame[cy, cx]            # Center of frame coordinate
    hue_value = pixel_center[0] 
    pixel_value = pixel_center[2]
        
    print("Hue: " + str(pixel_center[0]) + " Value: " + str(pixel_center[2]))
    
    color = "Undefined"
    if hue_value < 5:
        color = "RED"
    elif hue_value < 22:
        color = "ORANGE"
    elif hue_value < 33:
        color = "YELLOW"
    elif hue_value < 75 and pixel_value > 175:
        color = "LIME"
    elif hue_value < 75 and pixel_value < 175:
        color = "FOREST GREEN"
    elif hue_value < 93:
        color = "CYAN"
    elif hue_value < 131:
        color = "BLUE"
    elif hue_value < 148:
        color = "VIOLET"    
    elif hue_value < 170:
        color = "MAGENTA"
    else:
        color = "RED"
        
    pixel_center_bgr = frame[cy, cx]
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

    cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
    cv2.putText(frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5)
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

    cv2.imshow("Frame", frame)              # Frame display

    if cv2.waitKey(1) & 0xFF == ord('q'):   # Wait for user interrupt to close window
        break
 
 
# Destory and release 
  
cap.release()
cv2.destroyAllWindows()