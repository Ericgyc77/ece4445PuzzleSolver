import cv2

from PIL import Image

from util import get_limits

cap = cv2.VideoCapture(0) # Laptop webcam

orange = [0, 165, 255]  # yellow in BGR colorspace

# OpenCV interprets colors using BGR colorspace instead of RGB for some reason

while True:
    ret, frame = cap.read()
    
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lowerLimit, upperLimit = get_limits(color = orange)
    
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    
    mask_ = Image.fromarray(mask) # inbetween function
    
    bbox = mask_.getbbox() # enclose the masked object with a box, array with four points [x1, y1, x2, y2]
    
    if bbox is not None:
        x1, y1, x2, y2 = bbox # grab locations of bounding box

        # cv2.rectangle(frame, top left, bottom right, color, thickness)
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        
    print(bbox)
    
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()

cv2.destoryAllWindows()
