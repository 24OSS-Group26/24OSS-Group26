import cv2

def apply_mosaic_to_faces(image, scale=15, cascade_path="haarcascade_frontalface_default.xml"):
    # Load Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascade_path)

    # Convert the image to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Apply mosaic to each detected face
    for (x, y, w, h) in faces:
        # Extract the face region
        face_region = image[y:y + h, x:x + w]

        # Apply mosaic to the face region
        face_region = cv2.resize(face_region, (w // scale, h // scale), interpolation=cv2.INTER_LINEAR)
        face_region = cv2.resize(face_region, (w, h), interpolation=cv2.INTER_NEAREST)

        # Replace the face region with the mosaic version
        image[y:y + h, x:x + w] = face_region

    return image
