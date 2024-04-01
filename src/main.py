import cv2
import numpy as np
import time

from PIL import Image

from util import get_limits

cap = cv2.VideoCapture(1) # Laptop webcam

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

orange = [0, 165, 255]  # orange in BGR colorspace

# OpenCV interprets colors using BGR colorspace instead of RGB for some reason

while True:
    ret, frame = cap.read()
    
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lowerLimit, upperLimit = get_limits(color = orange)
    
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter out small contours
    min_area = 60  # Minimum area of contour to be considered, adjust as needed
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    
    # Create a new mask with only the large contours
    filtered_mask = np.zeros_like(mask)
    cv2.drawContours(filtered_mask, filtered_contours, -1, (255), thickness=cv2.FILLED)
    
    # Find the bounding box from the filtered mask
    x, y, w, h = cv2.boundingRect(filtered_mask)
    if w > 0 and h > 0:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
        # print((x, y, x + w, y + h))
    
    cv2.imshow('frame', filtered_mask)
    
    cv2.imshow('frame2', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()

cv2.destoryAllWindows()
