# TODO: Filter Application Updates
* ~~수정 완료하셨으면 취소선 표시 부탁드립니다!~~
* 여기 있는 거 이외에 수정할 사항이 있으면, 여기 적어주세요

## 1. **`cartoon.py` 수정 (잘 안되는 사진이 있음)**
- 문제: `cartoon.py` 필터가 일부 이미지에 대해 잘 작동하지 않음.

- 
## 2. ~~**이미지 오픈 왼쪽 정렬, 이미지 세이브 우측 정렬**~~
- 수정 사항: 
  - ~~"Open Image" 버튼을 왼쪽 정렬.~~
  - ~~"Save Image" 버튼을 우측 정렬.~~

## 3. **필터 버튼들 중앙 정렬**
- 수정 사항: 필터 버튼들이 중앙에 정렬되도록 `grid` 레이아웃 수정.

## 4. ~~**이미 적용된 필터 버튼 누르면 적용 취소되는 기능 추가**~~
- 수정 사항: 
  - ~~이미 적용된 필터 버튼을 누르면 필터가 취소되고 원본 이미지로 되돌려지도록 기능 추가.~~

## 5. **총 필터 개수는 15개로 5x3 으로 하면 좋을 거 같습니다**
- 수정 사항: 지금 만들어둔 필터가 12개라서 추가할 3개는 얼굴이나 사람 인식 기능이 들어간 필터면 좋을 거 같습니다.
  - **얼굴 인식 관련 코드** (코드는 아래와 mosaic.py 참고)

### Mediapipe 기반 얼굴 인식 코드 통합
'''
import mediapipe as mp
import cv2
import numpy as np

def detect_faces(image):
    """
    Detect faces in an image using Mediapipe Face Detection.

    Parameters:
        image (numpy.ndarray): Input image in BGR format.

    Returns:
        list: A list of detected face bounding boxes in (x, y, width, height) format.
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

    faces = []
    if results.detections:
        for detection in results.detections:
            # Get bounding box coordinates
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = image.shape
            x = int(bboxC.xmin * iw)
            y = int(bboxC.ymin * ih)
            w = int(bboxC.width * iw)
            h = int(bboxC.height * ih)

            # Ensure coordinates are within image bounds
            x, y = max(0, x), max(0, y)
            w, h = min(iw - x, w), min(ih - y, h)

            faces.append((x, y, w, h))

    # Release Mediapipe resources
    face_detection.close()

    return faces
'''

**얼굴인식 필터 아이디어 예시:**
1. Blur Background, Focus on 사람. (인물모드 느낌)

