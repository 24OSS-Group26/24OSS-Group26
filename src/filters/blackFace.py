import cv2
import numpy as np

def apply_black_face(image):
    """
    입력 이미지를 받아 얼굴을 검게 칠한 후 처리된 이미지를 반환합니다.

    :param image: 처리할 OpenCV 이미지 객체 (numpy.ndarray)
    :return: 얼굴이 검게 칠해진 OpenCV 이미지 객체
    """
    # OpenCV의 기본 얼굴 검출기 로드
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # 이미지 유효성 검사
    if image is None or not isinstance(image, np.ndarray):
        raise ValueError("유효하지 않은 이미지입니다.")

    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 얼굴 검출
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 얼굴 영역 검게 칠하기
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)

    return image
