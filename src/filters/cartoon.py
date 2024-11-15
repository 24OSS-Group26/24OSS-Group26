# 딥러닝 기반으로 변경하는 게 좋을 듯.
import cv2

def apply_cartoon_filter(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply median blur
    gray_blurred = cv2.medianBlur(gray, 7)

    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(gray_blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Reduce noise and create a cartoon effect
    color = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)

    # Combine edges and color
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon



'''
import os
import cv2
import numpy as np
import tensorflow as tf
import requests

MODEL_URL = "https://github.com/TachibanaYoshino/AnimeGANv2/releases/download/v2.0/AnimeGANv2_Hayao_99.tflite"
MODEL_PATH = "animeganv2_hayao.tflite"


def download_model(url, save_path):
    """
    AnimeGANv2 모델 파일을 다운로드하는 함수
    """
    if not os.path.exists(save_path):
        print("Downloading AnimeGANv2 model...")
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print("Model downloaded successfully!")
            else:
                raise RuntimeError(f"Failed to download model: {response.status_code}")
        except Exception as e:
            raise RuntimeError(f"Error downloading model: {e}")
    else:
        print("Model already exists. Skipping download.")

def load_tflite_model(model_path):
    """
    TensorFlow Lite 모델 로드 함수
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def apply_cartoon_filter(image):
    """
    AnimeGANv2 필터를 적용하는 함수 (apply_cartoon_filter와 동일하게 사용 가능)
    """
    # 모델 다운로드
    download_model(MODEL_URL, MODEL_PATH)

    # TensorFlow Lite 모델 로드
    interpreter = load_tflite_model(MODEL_PATH)

    # 모델 입력/출력 정보 가져오기
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # 모델 입력 크기 가져오기
    input_shape = input_details[0]['shape']
    height, width = input_shape[1], input_shape[2]

    # 이미지를 모델 입력 크기에 맞게 조정
    input_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(input_image, (width, height))
    input_data = np.expand_dims(resized_image / 127.5 - 1.0, axis=0).astype(np.float32)

    # 모델 실행
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # 결과 가져오기
    output_data = interpreter.get_tensor(output_details[0]['index'])[0]
    anime_image = ((output_data + 1.0) * 127.5).astype(np.uint8)

    # 원본 크기로 다시 조정
    anime_image = cv2.resize(anime_image, (image.shape[1], image.shape[0]))
    anime_image = cv2.cvtColor(anime_image, cv2.COLOR_RGB2BGR)

    return anime_image

'''
'''
import os
import cv2
import numpy as np
import tensorflow as tf
import requests

# 모델 URL과 로컬 저장 경로
MODEL_URL = "https://tfhub.dev/sayakpaul/lite-model/cartoongan/dr/1?lite-format=tflite"
MODEL_PATH = "cartoongan.tflite"

def download_model(url, save_path):
    """
    모델 파일을 다운로드하는 함수
    """
    if not os.path.exists(save_path):
        print("Downloading CartoonGAN model...")
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print("Model downloaded successfully!")
            else:
                raise RuntimeError(f"Failed to download model: {response.status_code}")
        except Exception as e:
            raise RuntimeError(f"Error downloading model: {e}")
    else:
        print("Model already exists. Skipping download.")

def load_tflite_model(model_path):
    """
    TensorFlow Lite 모델 로드 함수
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def apply_cartoon_filter(image):
    """
    Deep Learning 기반 CartoonGAN 필터 적용 함수
    """
    # 모델 다운로드
    download_model(MODEL_URL, MODEL_PATH)

    # TensorFlow Lite 모델 로드
    interpreter = load_tflite_model(MODEL_PATH)

    # 모델 입력/출력 정보 가져오기
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # 모델 입력 크기 가져오기
    input_shape = input_details[0]['shape']
    height, width = input_shape[1], input_shape[2]

    # 이미지를 모델 입력 크기에 맞게 조정
    input_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(input_image, (width, height))
    input_data = np.expand_dims(resized_image / 255.0, axis=0).astype(np.float32)

    # 모델 실행
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # 결과 가져오기
    output_data = interpreter.get_tensor(output_details[0]['index'])[0]
    cartoon_image = (output_data * 255).astype(np.uint8)

    # 원본 크기로 다시 조정
    cartoon_image = cv2.resize(cartoon_image, (image.shape[1], image.shape[0]))
    cartoon_image = cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR)

    return cartoon_image


'''


'''
import cv2
import numpy as np

def apply_cartoon_filter(image):
    # 1. 그레이스케일 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. 블러링을 통해 노이즈 제거
    gray_blurred = cv2.medianBlur(gray, 7)

    # 3. 엣지 감지 (적응형 임계값)
    edges = cv2.adaptiveThreshold(
        gray_blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=9, C=10
    )

    # 4. 양방향 필터로 부드러운 색상 영역 생성
    color = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)

    # 5. 엣지와 색상 결합
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon

'''




'''
import cv2

def apply_cartoon_filter(image):
    # 1. LAB 색 공간으로 변환
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_image)

    # 2. L 채널에 히스토그램 평활화 적용 (밝기 보정)
    l = cv2.equalizeHist(l)

    # 3. A와 B 채널에 약간의 대비 조정
    a = cv2.normalize(a, None, alpha=120, beta=135, norm_type=cv2.NORM_MINMAX)
    b = cv2.normalize(b, None, alpha=120, beta=135, norm_type=cv2.NORM_MINMAX)

    # 4. 보정된 LAB 이미지 다시 병합 및 BGR로 변환
    lab_image = cv2.merge((l, a, b))
    image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR)

    # 5. OpenCV의 stylization 필터 적용
    cartoon_image = cv2.stylization(image, sigma_s=150, sigma_r=0.25)

    return cartoon_image
'''




'''
import cv2

def apply_cartoon_filter(image):
    """
    제한 없이 어떤 이미지에도 적용 가능한 카툰 필터.
    기본 대비 보정 후 OpenCV의 stylization 기능을 활용.
    """
    # 1. 색상 대비 보정
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.equalizeHist(l)  # 밝기 채널에 히스토그램 평활화 적용
    lab = cv2.merge((l, a, b))
    image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # 2. 카툰 필터 적용 (OpenCV의 stylization 함수 사용)
    cartoon_image = cv2.stylization(image, sigma_s=150, sigma_r=0.25)

    return cartoon_image
'''
'''
# filters/cartoon.py
import cv2
import numpy as np
from skimage import exposure  # 추가: 색상 보정과 대비 조정을 위해 사용

def apply_cartoon_filter(image):
    # 1. 색상 보정: 대비 조정을 통해 생동감 있는 이미지를 생성
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # OpenCV는 기본적으로 BGR 사용
    image = exposure.adjust_sigmoid(image, cutoff=0.5, gain=10, inv=False)  # 대비 강화
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # 다시 BGR로 변환

    # 2. 이미지 그레이스케일 변환 및 잡음 제거
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # 3. 윤곽선 감지: Canny Edge Detection으로 선명한 경계선 생성
    edges = cv2.Canny(gray_blurred, threshold1=50, threshold2=150)

    # 4. 윤곽선 확장: 윤곽선의 두께를 늘려 효과를 강조
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)

    # 5. 카툰 스타일 적용: 양방향 필터로 부드러운 색상 영역 생성
    color = cv2.bilateralFilter(image, d=15, sigmaColor=75, sigmaSpace=75)

    # 6. 윤곽선과 색상을 결합하여 카툰 효과 생성
    edges_inverse = cv2.bitwise_not(edges_dilated)  # 흰색 배경의 검은 윤곽선으로 반전
    cartoon = cv2.bitwise_and(color, color, mask=edges_inverse)

    return cartoon
'''
