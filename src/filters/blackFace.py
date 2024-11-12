import cv2
import mediapipe as mp
import numpy as np

def apply_black_circle_to_faces(image):
    """
    Apply a black circle to cover detected faces in an image using Mediapipe Face Detection.

    Parameters:
        image (numpy.ndarray): Input image in BGR format.

    Returns:
        numpy.ndarray: Image with black circles applied to detected faces.
    """
    if not isinstance(image, np.ndarray):
        raise TypeError("Input image must be a numpy.ndarray.")

    # Initialize Mediapipe Face Detection
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7)

    # Convert the image to RGB (Mediapipe requires RGB format)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform face detection
    results = face_detection.process(rgb_image)

    # If faces are detected, apply black circle
    if results.detections:
        for detection in results.detections:
            try:
                # Get bounding box coordinates
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)

                # Ensure coordinates are within image bounds
                x, y = max(0, x), max(0, y)
                x2, y2 = min(iw, x + w), min(ih, y + h)

                # Calculate the center and radius of the circle
                center = (x + w // 2, y + h // 2)
                radius = min(w, h) // 2

                # Draw a black circle on the face region
                cv2.circle(image, center, radius, (0, 0, 0), -1)

            except Exception as e:
                print(f"Error applying black circle to a face: {e}")

    # Release Mediapipe resources
    face_detection.close()

    return image
