import numpy as np
import cv2

def canny(image_input):

    # parameters for canny edge detection
    low_threshold = 100
    high_threshold = 200
    # do canny edge detection
    image_canny = cv2.Canny(image_input, low_threshold, high_threshold)
    return image_canny


