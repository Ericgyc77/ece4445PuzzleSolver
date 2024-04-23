import cv2
import numpy as np
import time
import serialComm  # Import the serial communication functions

# Initialize serial communication
ser = serialComm.init_serial('/dev/ttyACM0', 9600)

cap = cv2.VideoCapture(-1) # Webcam, needs to be changed from PC to laptop

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

# Define hue and value ranges for detection, ignoring saturation
color_ranges = {
    'red': [([0, 100, 100], [8, 255, 255], (0, 0, 255))],
    'orange': [([9, 100, 100], [19, 255, 255], (0, 165, 255))],
    'yellow': [([20, 100, 100], [33, 255, 255], (0, 255, 255))],
    'lime_green': [([34, 100, 40], [58, 255, 225], (0, 255, 0))],
    'dark_green': [([59, 100, 100], [74, 255, 225], (0, 128, 0))],
    'cyan': [([75, 100, 100], [101, 255, 255], (255, 255, 0))],         # STRONGGG
    'blue': [([102, 100, 100], [120, 255, 255], (255, 0, 0))],
    'violet': [([137, 60, 100], [169, 255, 255], (255, 0, 255))],       # deep violet
    'magenta': [([170, 70, 100], [178, 255, 255], (255, 0, 255))],      # florescent magenta
}

################################################ Executive Loop #######################################################

last_sent = time.time()
last_noticeUpdate = time.time()
send_interval = 1                               # send every 1 seconds

while True:
    ret, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, ret = frame.shape
    
    cx = int(width / 2)
    cy = int(height / 2)

    pixel_center = hsv_frame[cy, cx]            # Absolute center of camera frame of reference
    
    ################################################ Start of HSV Algorithm ################################################
    
    # Define color ranges for detection

    colorDetected = False
    
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
            if cv2.contourArea(contour) > 300:  # Filter out small areas
                x, y, w, h = cv2.boundingRect(contour)
                area = w * h
                if area > largest_area:
                    largest_area = area
                    largest_rect = (x, y, w, h)
                cv2.rectangle(frame, (x, y), (x + w, y + h), bbox_color, 2)  # Draw rectangle in bbox_color
                colorDetected = True
                # if (float(time.time() - last_noticeUpdate) > float(send_interval)):
                #     print("Attempting to send notice.")
                #     notice = serialComm.receive_message(ser)
                #     # Check for and print response from Arduino
                #     if notice:
                #         print("NOTICE: " + str(notice))       
                #     last_noticeUpdate = time.time()     

                # Check that send interval has elapsed before new color detection message is sent
                if colorDetected:
                    # Send and receive messages via serial
                    request = serialComm.receive_message(ser)
                    # Check for request for color signal from Arduino
                    if (request == 'R'):
                        serialComm.send_message(ser, str(color_name))
                        print("Sent color " + str(color_name) + " to Arduino!")
                        response = serialComm.receive_message(ser)
                        # Check for and print response from Arduino
                        if response:
                            print("Response from Arduino: " + str(response))


                           
                
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
            # print("Distance from center:", distance)

        
            
    ################################################ End of HSV Algorithm ##################################################

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
serialComm.close_serial(ser)