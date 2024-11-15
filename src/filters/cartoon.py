import os
import cv2
import numpy as np
import tensorflow as tf
import requests

# 모델 URL과 로컬 저장 경로
MODEL_URL = "https://tfhub.dev/sayakpaul/lite-model/cartoongan/dr/1?lite-format=tflite"
MODEL_PATH = "cartoongan.tflite"

def download_model(url, save_path):
  
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
 
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def apply_cartoon_filter(image):
   
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

