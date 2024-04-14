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
    'red': [([0, 100, 100], [8, 255, 255], (0, 0, 255))],
    'orange': [([9, 100, 100], [19, 255, 255], (0, 165, 255))],
    'yellow': [([20, 100, 100], [33, 255, 255], (0, 255, 255))],
    'lime_green': [([34, 100, 40], [58, 255, 225], (0, 255, 0))],
    'dark_green': [([59, 100, 100], [74, 255, 225], (0, 128, 0))],
    'cyan': [([75, 100, 100], [101, 255, 255], (255, 255, 0))],   # STRONGGG
    'blue': [([102, 100, 100], [120, 255, 255], (255, 0, 0))],
    'violet': [([137, 60, 100], [169, 255, 255], (255, 0, 255))], # more like light magenta
    'magenta': [([170, 70, 100], [178, 255, 255], (255, 0, 255))], # florescent magenta
}

# Change one of the magenta's, preferabbly lighter shade of magenta with a color lower on the hue scale more towards violet

################################################ Executive Loop #######################################################

while True:
    ret, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, ret = frame.shape
    
    cx = int(width / 2)
    cy = int(height / 2)

    pixel_center = hsv_frame[cy, cx]            # Absolute center of camera frame of reference
    
    ################################################ Start of HSV Algorithm ################################################
    
    # Define color ranges for detection
    
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
            
            ################################################ End of HSV Algorithm ##################################################
            ######################################## Start of Robot Movement Calculation ###########################################

            
            # calculate the distance that the robot arm needs to move to reach the puzzle piece
            # translate the pixel distance from the camera's center to the puzzle piece into real-world measurements
            # scaling the pixel distance by a factor that translates it to the actual distance on the puzzle board.
            # add offset of camera to robot arm as a vector to the scaled pixel distance to get the total distance to move
            
            # Using cm as our real world units, assume everything is in cm unless stated otherwise
            
            # x move right 8cm
            # y move up 5 cm
            
            # Beginning of scale factor
            # Current Calibration -> 185.647 pixel distance translates to 4cm
            # Scale factor = 46.41175 pixels/cm
            
            # Need to determine heading: 
            # Right side of screen will be postive X, left will be negative
            # FOrward positive, backward negative
            
            
            # Variables defined TBD when real world measurements are made
            scale_factor = 0.02154627       # scale factor to convert pixels to cm
            offset_x = 8                    # Horizontal offset of the robot arm (cm)
            offset_y = 5                    # Vertical offset of the robot arm (cm)
            
            # cx and cy represent absolute center of camera 
            distance_x_in_pixels = frame_center_x - cx  # Center of camera x-coordinate in pixels
            distance_y_in_pixels = frame_center_y - cy # Center of camera y-coordinate in pixels
            
            # Convert pixel distances to real-world units
            distance_x_in_units = distance_x_in_pixels * scale_factor
            distance_y_in_units = distance_y_in_pixels * scale_factor
            
            # Calculate the total distance the robot arm needs to move, including the offset
            total_distance_x = distance_x_in_units + offset_x
            total_distance_y = distance_y_in_units + offset_y
            
            ######################################## End of Robot Movement Calculation ###########################################
    ####################################################### DEBUG ########################################################
    
    hue_value = pixel_center[0] 
    pixel_value = pixel_center[2]
    
    # uncomment for verbose terminal for HSV troubleshooting
    # print("Hue: " + str(pixel_center[0]) + " Saturation: " + str(pixel_center[1]) +  " Value: " + str(pixel_center[2]))
    
    #################################################### END OF DEBUG ####################################################

    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

    cv2.imshow("Frame", frame)              # Frame display

    if cv2.waitKey(1) & 0xFF == ord('q'):   # Wait for user interrupt to close window
        break
    
################################################# End of Executive Loop ##################################################
 
# Destory and release  
cap.release()
cv2.destroyAllWindows()