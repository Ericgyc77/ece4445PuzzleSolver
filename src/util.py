import numpy as np
import cv2

def get_hsv_limits(hue, saturation_range=(100, 255), value_range=(100, 255), hue_margin=10):
    lower_limit = np.array([hue - hue_margin, saturation_range[0], value_range[0]], dtype=np.uint8)
    upper_limit = np.array([hue + hue_margin, saturation_range[1], value_range[1]], dtype=np.uint8)
    return lower_limit, upper_limit


    