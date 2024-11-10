import cv2
import numpy as np
import mediapipe as mp


def apply_portrait_mode(image):
    """
    Blur all areas except detected persons (body) in the image.

    Parameters:
        image (numpy.ndarray): Input image in BGR format.

    Returns:
        numpy.ndarray: Image with non-person areas blurred.
    """
    # Initialize Mediapipe Selfie Segmentation
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    # Convert the image to RGB for Mediapipe
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform segmentation
    results = segmentation.process(rgb_image)

    # Generate mask for the person
    condition = results.segmentation_mask > 0.5  # Segmentation threshold
    mask = np.where(condition, 255, 0).astype(np.uint8)

    # Invert the mask (non-person areas become white)
    mask_inv = cv2.bitwise_not(mask)

    # Blur the entire image
    blurred_image = cv2.GaussianBlur(image, (51, 51), 0)

    # Combine the original image and blurred image using the masks
    person_areas = cv2.bitwise_and(image, image, mask=mask)
    non_person_areas = cv2.bitwise_and(blurred_image, blurred_image, mask=mask_inv)

    # Release Mediapipe resources
    segmentation.close()

    return cv2.add(person_areas, non_person_areas)
