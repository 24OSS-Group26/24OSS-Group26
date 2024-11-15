import cv2

def apply_black_face(image_path, output_path):
    # OpenCV의 기본 얼굴 검출기 로드 (Haar Cascade)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # 이미지 읽기
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("이미지를 읽을 수 없습니다. 경로를 확인하세요.")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 얼굴 검출
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 얼굴을 검게 칠하기
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)

    # 결과 저장
    cv2.imwrite(output_path, image)
    print(f"결과 이미지가 {output_path}에 저장되었습니다.")
