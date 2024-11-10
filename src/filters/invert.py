import cv2

def apply_invert_filter(image):
    return cv2.bitwise_not(image)
