from PIL import Image
import os


def create_gif(image_folder, output_gif_path, duration=500):
    # 현재 폴더에 있는 모든 .png 파일을 가져옵니다.
    image_files = [f"{i}.png" for i in range(1, 18)]  # 1.png부터 17.png까지 예시 (필요에 따라 범위 조정)

    images = []

    # 각 이미지를 열고 리스트에 추가합니다.
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        if os.path.exists(image_path):
            image = Image.open(image_path)
            images.append(image)
        else:
            print(f"파일이 존재하지 않습니다: {image_path}")
            return

    # 첫 번째 이미지에서 GIF로 저장
    images[0].save(output_gif_path, save_all=True, append_images=images[1:], duration=duration, loop=0)
    print(f"GIF 파일이 저장되었습니다: {output_gif_path}")


# 사용 예시
if __name__ == "__main__":
    # 현재 스크립트가 위치한 폴더 경로를 구합니다.
    current_folder = os.path.dirname(os.path.realpath(__file__))

    # GIF 파일을 생성할 경로
    output_gif_path = os.path.join(current_folder, "output.gif")  # 동일 폴더에 저장될 output.gif

    create_gif(current_folder, output_gif_path)
