import cv2
import numpy as np
import time

from PIL import Image

from util import get_limits

cap = cv2.VideoCapture(0) # Webcam, needs to be changed from PC to laptop

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


# Colors dictionary, first entry -> BGR colorspace, second entry -> RGB colorspace (for bounding boxes)

colors = {
    "red" : ([0, 0, 255], [0, 0, 200], "red"), # Detect red, draw bounding box in dark red
    # "blue" : ([255, 128, 0], [255, 255, 0], "blue"), # Detect blue, draw bounding box in cyan (WORKING)
    "green" : ([0, 40, 0], [0, 105, 0], "green"), # Detect green, draw bounding box in green 
    "lime" : ([0, 255, 0], [0, 213, 0], "lime"), # Detect lime, draw bounding box in darker lime (WORKING)
    "yellow" : ([0, 255, 255], [0, 200, 200], "yellow"), # Detect yellow, draw bounding box in darker yellow (WORKING)
    "orange" : ([0, 165, 255], [0, 69, 255], "orange"), # Detect orange, draw bounding box in darker orange (WORKING)
    "violet" : ([255, 0, 127], [148, 0, 211], "violet"), # Detect violet, draw bounding box in dark violet (WORKING)
}



# OpenCV interprets colors using BGR colorspace instead of RGB for some reason

while True:
    ret, frame = cap.read()
    
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    
    # find the limits of all colors
    # create all the masks needed
    for color_name, (bgr, bbox_color, name) in colors.items():
        
        lowerLimit, upperLimit = get_limits(color = bgr)
        
        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Filter out small contours
        min_area = 75  # Minimum area of contour to be considered, adjust as needed
        found = False
        for cnt in contours:
            if cv2.contourArea(cnt) > min_area:
                found = True
                x, y, w, h = cv2.boundingRect(cnt)
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), bbox_color, 3)
                
        if found:
            print(f"{name.capitalize()} has been found")
    
    
    
    
    # filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    # # Create a new mask with only the large contours
    # filtered_mask = np.zeros_like(mask)
    # cv2.drawContours(filtered_mask, filtered_contours, -1, (255), thickness=cv2.FILLED)
    
    # # Find the bounding box from the filtered mask
    # x, y, w, h = cv2.boundingRect(filtered_mask)
    # if w > 0 and h > 0:
    #     frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
    #     # print((x, y, x + w, y + h))
    
    # cv2.imshow('frame', filtered_mask)
    
    cv2.imshow('frame2', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()

cv2.destoryAllWindows()
