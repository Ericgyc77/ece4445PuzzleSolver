import cv2
import numpy as np
import time

from util import create_mask
from util import find_and_box_objects

cap = cv2.VideoCapture(1) # Webcam, needs to be changed from PC to laptop
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

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

# 'lime': [((34, 255, 175), (74, 255, 255))],
# 'red_wrap': [((171, 255, 255), (179, 255, 255)), (0, 0, 255)],

# Define hue and value ranges for detection, ignoring saturation
color_ranges = {
    'red': [([0, 100, 100], [5, 255, 255], (0, 0, 255))],
    'orange': [([6, 100, 100], [21, 255, 255], (0, 165, 255))],
    'yellow': [([22, 100, 100], [33, 255, 255], (0, 255, 255))],
    'green': [([34, 100, 40], [74, 255, 174], (0, 128, 0))],
    'cyan': [([75, 100, 100], [101, 255, 255], (255, 255, 0))],   # STRONGGG
    'blue': [([102, 100, 100], [120, 255, 255], (255, 0, 0))],
    'violet': [([150, 100, 100], [169, 255, 255], (255, 0, 255))], # more like light magenta
    'magenta': [([170, 100, 100], [178, 255, 255], (255, 0, 255))], # florescent magenta
}

# Change one of the magenta's, preferabbly lighter shade of magenta with a color lower on the hue scale more towards violet


while True:
    ret, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, ret = frame.shape
    
    ################################################ START OF NEW CODE ######################################################
    
    # Define color ranges for detection
    # Example for yellow (like a banana)
    # yellow_lower = np.array([162, 100, 100])
    # yellow_upper = np.array([178, 255, 255])
    # yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)
    
    # cv2.imshow('Mask', yellow_mask)
    
    for color_name, ranges in color_ranges.items():
        mask = None
        for lower, upper, bbox_color in ranges:
            temp_mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))
            if mask is None:
                mask = temp_mask
            else:
                mask = cv2.bitwise_or(mask, temp_mask)
    
        largest_area = 0
        largest_rect = None
        
        # Find contours and draw bounding box for yellow objects
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Filter out small areas
                x, y, w, h = cv2.boundingRect(contour)
                area = w * h
                if area > largest_area:
                    largest_area = area
                    largest_rect = (x, y, w, h)
                cv2.rectangle(frame, (x, y), (x + w, y + h), bbox_color, 2)  # Draw rectangle in yellow
                
        if largest_rect is not None:
            x, y, w, h = largest_rect
            center_x = x + w // 2               # find center of largest rectangle, flooring division 
            center_y = y + h // 2
        
            # Draw a dot at the center of the largest bounding box
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            # Calculate the distance from the absolute center of the frame
            frame_center_x = width // 2
            frame_center_y = height // 2
            distance = ((center_x - frame_center_x) ** 2 + (center_y - frame_center_y) ** 2) ** 0.5
            
            # Optionally, you can print or display the distance on the frame
            print("Distance from center:", distance)
            
    ################################################ END OF NEW CODE ######################################################

    ################################################ START OF OLD CODE ######################################################

    cx = int(width / 2)
    cy = int(height / 2)

    # Pick pixel value
    pixel_center = hsv_frame[cy, cx]            # Center of frame coordinate
    hue_value = pixel_center[0] 
    pixel_value = pixel_center[2]
        
    # print("Hue: " + str(pixel_center[0]) + " Saturation: " + str(pixel_center[1]) +  " Value: " + str(pixel_center[2]))
    
    # color = "Undefined"
    # if hue_value < 5:
    #     color = "RED"
    # elif hue_value < 22:
    #     color = "ORANGE"
    # elif hue_value < 33:
    #     color = "YELLOW"
    # elif hue_value < 75 and pixel_value > 175:
    #     color = "LIME"
    # elif hue_value < 75 and pixel_value < 175:
    #     color = "GREEN"
    # elif hue_value < 93:
    #     color = "CYAN"
    # elif hue_value < 131:
    #     color = "BLUE"
    # elif hue_value < 148:
    #     color = "VIOLET"    
    # elif hue_value < 170:
    #     color = "MAGENTA"
    # else:
    #     color = "RED"
        
    # pixel_center_bgr = frame[cy, cx]
    # b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
    # cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
    # cv2.putText(frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5)
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

    cv2.imshow("Frame", frame)              # Frame display

    if cv2.waitKey(1) & 0xFF == ord('q'):   # Wait for user interrupt to close window
        break
 
 
# Destory and release  
cap.release()
cv2.destroyAllWindows()