import numpy as np
import cv2

def create_mask(hsv_frame, lower_color, upper_color):
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    return mask

def find_and_box_objects(frame, mask, color):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Threshold to filter small contours
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    