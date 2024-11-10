import cv2

def apply_mosaic(image, scale=15):
    h, w, _ = image.shape
    mosaic_image = cv2.resize(image, (w // scale, h // scale), interpolation=cv2.INTER_LINEAR)
    mosaic_image = cv2.resize(mosaic_image, (w, h), interpolation=cv2.INTER_NEAREST)
    return mosaic_image
