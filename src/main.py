import customtkinter as ctk
from tkinter import filedialog, messagebox
import cv2
from filters.mosaic import apply_mosaic_to_faces
from filters.grayscale import apply_grayscale
from filters.cartoon import apply_cartoon_filter
from filters.sketch import apply_sketch_filter
from filters.invert import apply_invert_filter
from filters.blur import apply_blur
from filters.edge_detection import apply_edge_detection
from filters.sepia import apply_sepia
from filters.brightness import apply_brightness
from filters.saturation import apply_saturation
from filters.hdr_effect import apply_hdr_effect
from filters.vignette import apply_vignette
from filters.portrait_mode import apply_portrait_mode
from PIL import Image, ImageTk
import numpy as np


class FilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Filter Application")
        self.root.geometry("1000x800")
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.image = None
        self.cv_image = None
        self.original_image = None
        self.current_filter = "None"

        self.init_gui()

    def init_gui(self):
        # Title
        title_label = ctk.CTkLabel(self.root, text="Photo Filter Application", font=("Arial", 28, "bold"),
                                   text_color="#1abc9c")
        title_label.grid(row=0, column=0, pady=10, sticky="n")

        # Top buttons (Open & Save)
        button_frame_top = ctk.CTkFrame(self.root, fg_color="transparent")
        button_frame_top.grid(row=1, column=0, pady=5, sticky="ew")
        button_frame_top.columnconfigure(0, weight=1)
        button_frame_top.columnconfigure(1, weight=1)
        button_frame_top.columnconfigure(2, weight=1)

        btn_open = ctk.CTkButton(button_frame_top, text="Open Image", command=self.open_image, width=180,
                                 fg_color="#27ae60")  # Open 버튼 색상 유지
        btn_open.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        btn_save = ctk.CTkButton(button_frame_top, text="Save Image", command=self.save_image, width=180,
                                 fg_color="#3498db")  # Save 버튼 색상 유지
        btn_save.grid(row=0, column=2, padx=15, pady=10, sticky="e")

        # Canvas Frame
        self.canvas_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.canvas_frame.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg="gray", bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Bind resize event
        self.canvas_frame.bind("<Configure>", self.on_resize)

        # Current Filter Label
        self.filter_label = ctk.CTkLabel(self.root, text=f"Current Filter: {self.current_filter}",
                                         font=("Arial", 16), text_color="#00d2d3")
        self.filter_label.grid(row=3, column=0, pady=5, sticky="n")

        # Filter Buttons
        button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        button_frame.grid(row=4, column=0, pady=10, sticky="ew")
        button_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        filters = [
            ("Mosaic", self.apply_mosaic_filter),
            ("Grayscale", self.apply_grayscale_filter),
            ("Cartoon", self.apply_cartoon_filter),
            ("Sketch", self.apply_sketch_filter),
            ("Invert", self.apply_invert_filter),
            ("Blur", self.apply_blur_filter),
            ("Edge", self.apply_edge_filter),
            ("Sepia", self.apply_sepia_filter),
            ("Brightness", self.apply_brightness_filter),
            ("Saturation", self.apply_saturation_filter),
            ("HDR", self.apply_hdr_filter),
            ("Vignette", self.apply_vignette_filter),
            ("Portrait Mode", self.apply_portrait_mode),
            ("추가2", self.apply_additional_filter2),
            ("추가3", self.apply_additional_filter3),
        ]

        # Modify padding and button size
        button_width = 180  # 줄인 버튼 크기
        for i, (text, command) in enumerate(filters):
            ctk.CTkButton(button_frame, text=f"{text} Filter", command=command, width=button_width).grid(
                row=i // 5, column=i % 5, padx=10, pady=5, sticky="nsew"
            )


        footer_label = ctk.CTkLabel(self.root, text="Tip: Open an image, apply a filter, and save it!",
                                    font=("Arial", 14), text_color="#bdc3c7")
        footer_label.grid(row=5, column=0, pady=10, sticky="n")

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if not file_path:
            return
        try:
            file_data = np.fromfile(file_path, dtype=np.uint8)
            self.original_image = cv2.imdecode(file_data, cv2.IMREAD_COLOR)
            if self.original_image is None:
                raise ValueError("Failed to decode the image.")
            self.original_file_path = file_path  # 파일 경로 저장
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open the image: {e}")
            return

        self.cv_image = self.original_image.copy()
        self.current_filter = "None"
        self.update_filter_label()
        self.display_image()

    def display_image(self):
        if self.cv_image is not None:
            rgb_image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_image)
            canvas_width, canvas_height = self.canvas_frame.winfo_width(), self.canvas_frame.winfo_height()
            image_ratio = image.width / image.height
            canvas_ratio = canvas_width / canvas_height

            if image_ratio > canvas_ratio:
                new_width = canvas_width
                new_height = int(canvas_width / image_ratio)
            else:
                new_height = canvas_height
                new_width = int(canvas_height * image_ratio)

            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.image = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.image)

    def update_filter_label(self):
        self.filter_label.configure(text=f"Current Filter: {self.current_filter}")

    def apply_filter(self, filter_function, filter_name):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Open an image first!")
            return
        if self.current_filter == filter_name:
            self.cv_image = self.original_image.copy()
            self.current_filter = "None"
        else:
            self.cv_image = filter_function(self.original_image.copy())
            self.current_filter = filter_name
        self.update_filter_label()
        self.display_image()

    def apply_mosaic_filter(self):
        self.apply_filter(apply_mosaic_to_faces, "Mosaic")

    def apply_grayscale_filter(self):
        self.apply_filter(apply_grayscale, "Grayscale")

    def apply_cartoon_filter(self):
        self.apply_filter(apply_cartoon_filter, "Cartoon")

    def apply_sketch_filter(self):
        self.apply_filter(apply_sketch_filter, "Sketch")

    def apply_invert_filter(self):
        self.apply_filter(apply_invert_filter, "Invert")

    def apply_blur_filter(self):
        self.apply_filter(apply_blur, "Blur")

    def apply_edge_filter(self):
        self.apply_filter(apply_edge_detection, "Edge")

    def apply_sepia_filter(self):
        self.apply_filter(apply_sepia, "Sepia")

    def apply_brightness_filter(self):
        self.apply_filter(apply_brightness, "Brightness")

    def apply_saturation_filter(self):
        self.apply_filter(apply_saturation, "Saturation")

    def apply_hdr_filter(self):
        self.apply_filter(apply_hdr_effect, "HDR")

    def apply_vignette_filter(self):
        self.apply_filter(apply_vignette, "Vignette")

    def apply_portrait_mode(self):
        self.apply_filter(apply_portrait_mode, "Portrait Mode")  # Link the new filter

    def apply_additional_filter2(self):
        self.apply_filter(lambda img: img, "추가2")

    def apply_additional_filter3(self):
        self.apply_filter(lambda img: img, "추가3")

    def save_image(self):
        if self.cv_image is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
        if self.current_filter == "None":
            messagebox.showwarning("Warning", "No filter applied!")
            return

        # 파일명을 가져와서 적용된 필터를 추가한 새로운 이름 생성
        if hasattr(self, 'original_file_path'):
            original_name = self.original_file_path.split("/")[-1].split(".")[0]  # 파일명(확장자 제외)
        else:
            original_name = "image"  # 기본 이름

        new_filename = f"{original_name}_{self.current_filter}.png"  # 필터 이름 포함 저장 파일명 생성

        # 사용자에게 저장 위치 및 파일명 선택 요청
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 initialfile=new_filename,
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if not file_path:
            return
        cv2.imwrite(file_path, self.cv_image)  # 저장
        messagebox.showinfo("Info", f"Image saved successfully!")
        #messagebox.showinfo("Info", f"Image saved successfully as {file_path}!")

    def on_resize(self, event):
        """Callback for dynamically resizing the canvas when the window size changes."""
        self.display_image()


if __name__ == "__main__":
    root = ctk.CTk()
    app = FilterApp(root)
    root.mainloop()

'''
사진 여러장 로드 기능 테스트 중
import customtkinter as ctk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np

# 필터 함수들 (실제로 존재하는 필터 함수 사용)
from filters.mosaic import apply_mosaic_to_faces
from filters.grayscale import apply_grayscale
from filters.cartoon import apply_cartoon_filter
from filters.sketch import apply_sketch_filter
from filters.invert import apply_invert_filter
from filters.blur import apply_blur
from filters.edge_detection import apply_edge_detection
from filters.sepia import apply_sepia
from filters.brightness import apply_brightness
from filters.saturation import apply_saturation
from filters.hdr_effect import apply_hdr_effect
from filters.vignette import apply_vignette
from filters.portrait_mode import apply_portrait_mode


class FilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Filter Application")
        self.root.geometry("1000x800")
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.image = None
        self.cv_image = None
        self.original_image = None
        self.current_filter = "None"
        self.image_cache = []  # 여러 장 이미지 캐시

        self.init_gui()

    def init_gui(self):
        # Title
        title_label = ctk.CTkLabel(self.root, text="Photo Filter Application", font=("Arial", 28, "bold"),
                                   text_color="#1abc9c")
        title_label.grid(row=0, column=0, pady=10, sticky="n")

        # Top buttons (Open & Save)
        button_frame_top = ctk.CTkFrame(self.root, fg_color="transparent")
        button_frame_top.grid(row=1, column=0, pady=5, sticky="ew")
        button_frame_top.columnconfigure(0, weight=1)
        button_frame_top.columnconfigure(1, weight=1)
        button_frame_top.columnconfigure(2, weight=1)

        btn_open = ctk.CTkButton(button_frame_top, text="Open Image", command=self.open_image, width=180,
                                 fg_color="#27ae60")
        btn_open.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        btn_open_multi = ctk.CTkButton(button_frame_top, text="Open Multiple Images", command=self.open_multiple_images,
                                       width=180, fg_color="#2ecc71")
        btn_open_multi.grid(row=0, column=1, padx=15, pady=10, sticky="w")

        btn_save = ctk.CTkButton(button_frame_top, text="Save Image", command=self.save_image, width=180,
                                 fg_color="#3498db")
        btn_save.grid(row=0, column=2, padx=15, pady=10, sticky="e")

        # Canvas Frame
        self.canvas_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.canvas_frame.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg="gray", bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Bind resize event
        self.canvas_frame.bind("<Configure>", self.on_resize)

        # Current Filter Label
        self.filter_label = ctk.CTkLabel(self.root, text=f"Current Filter: {self.current_filter}",
                                         font=("Arial", 16), text_color="#00d2d3")
        self.filter_label.grid(row=3, column=0, pady=5, sticky="n")

        # Filter Buttons
        button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        button_frame.grid(row=4, column=0, pady=10, sticky="ew")
        button_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        filters = [
            ("Mosaic", self.apply_mosaic_filter),
            ("Grayscale", self.apply_grayscale_filter),
            ("Cartoon", self.apply_cartoon_filter),
            ("Sketch", self.apply_sketch_filter),
            ("Invert", self.apply_invert_filter),
            ("Blur", self.apply_blur_filter),
            ("Edge", self.apply_edge_filter),
            ("Sepia", self.apply_sepia_filter),
            ("Brightness", self.apply_brightness_filter),
            ("Saturation", self.apply_saturation_filter),
            ("HDR", self.apply_hdr_filter),
            ("Vignette", self.apply_vignette_filter),
            ("Portrait Mode", self.apply_portrait_mode),
            ("추가2", self.apply_additional_filter2),
            ("추가3", self.apply_additional_filter3),
        ]

        for i, (text, command) in enumerate(filters):
            ctk.CTkButton(button_frame, text=f"{text} Filter", command=command, width=180).grid(
                row=i // 5, column=i % 5, padx=10, pady=5, sticky="nsew"
            )

        footer_label = ctk.CTkLabel(self.root, text="Tip: Open images, apply a filter, and save them!",
                                    font=("Arial", 14), text_color="#bdc3c7")
        footer_label.grid(row=5, column=0, pady=10, sticky="n")

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if not file_path:
            return
        self.load_image(file_path)

    def open_multiple_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if not file_paths:
            return

        self.image_cache = []

        for file_path in file_paths:
            try:
                image = self.read_image(file_path)
                self.image_cache.append(image)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image {file_path}: {e}")

        self.display_gallery()

    def load_image(self, file_path):
        try:
            image = self.read_image(file_path)
            self.original_image = image
            self.cv_image = image.copy()
            self.current_filter = "None"
            self.update_filter_label()
            self.display_image()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def read_image(self, file_path):
        file_data = np.fromfile(file_path, dtype=np.uint8)
        return cv2.imdecode(file_data, cv2.IMREAD_COLOR)

    def display_gallery(self):
        new_window = ctk.CTkToplevel(self.root)
        new_window.title("Image Gallery")
        new_window.geometry("1200x800")

        gallery_frame = ctk.CTkFrame(new_window, fg_color="transparent")
        gallery_frame.pack(fill="both", expand=True)

        for i, img in enumerate(self.image_cache):
            rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_image).resize((150, 150), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(pil_image)

            label = ctk.CTkLabel(gallery_frame, image=tk_image, text=f"Image {i + 1}")
            label.grid(row=i // 4, column=i % 4, padx=10, pady=10)
            self.image_cache[i] = tk_image  # 이미지 캐시 유지

    def display_image(self):
        if self.cv_image is not None:
            rgb_image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_image)
            canvas_width, canvas_height = self.canvas_frame.winfo_width(), self.canvas_frame.winfo_height()
            image_ratio = image.width / image.height
            canvas_ratio = canvas_width / canvas_height

            if image_ratio > canvas_ratio:
                new_width = canvas_width
                new_height = int(canvas_width / image_ratio)
            else:
                new_height = canvas_height
                new_width = int(canvas_height * image_ratio)

            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.image = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.image)

    def update_filter_label(self):
        self.filter_label.configure(text=f"Current Filter: {self.current_filter}")

    def apply_filter(self, filter_function, filter_name):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Open an image first!")
            return
        if self.current_filter == filter_name:
            self.cv_image = self.original_image.copy()
            self.current_filter = "None"
        else:
            self.cv_image = filter_function(self.original_image.copy())
            self.current_filter = filter_name
        self.update_filter_label()
        self.display_image()

    def apply_mosaic_filter(self):
        self.apply_filter(apply_mosaic_to_faces, "Mosaic")

    def apply_grayscale_filter(self):
        self.apply_filter(apply_grayscale, "Grayscale")

    def apply_cartoon_filter(self):
        self.apply_filter(apply_cartoon_filter, "Cartoon")

    def apply_sketch_filter(self):
        self.apply_filter(apply_sketch_filter, "Sketch")

    def apply_invert_filter(self):
        self.apply_filter(apply_invert_filter, "Invert")

    def apply_blur_filter(self):
        self.apply_filter(apply_blur, "Blur")

    def apply_edge_filter(self):
        self.apply_filter(apply_edge_detection, "Edge")

    def apply_sepia_filter(self):
        self.apply_filter(apply_sepia, "Sepia")

    def apply_brightness_filter(self):
        self.apply_filter(apply_brightness, "Brightness")

    def apply_saturation_filter(self):
        self.apply_filter(apply_saturation, "Saturation")

    def apply_hdr_filter(self):
        self.apply_filter(apply_hdr_effect, "HDR")

    def apply_vignette_filter(self):
        self.apply_filter(apply_vignette, "Vignette")

    def apply_portrait_mode(self):
        self.apply_filter(apply_portrait_mode, "Portrait Mode")

    def apply_additional_filter2(self):
        self.apply_filter(lambda img: img, "추가2")

    def apply_additional_filter3(self):
        self.apply_filter(lambda img: img, "추가3")

    def save_image(self):
        if self.cv_image is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
        if self.current_filter == "None":
            messagebox.showwarning("Warning", "No filter applied!")
            return

        if hasattr(self, 'original_file_path'):
            original_name = self.original_file_path.split("/")[-1].split(".")[0]
        else:
            original_name = "image"

        new_filename = f"{original_name}_{self.current_filter}.png"
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 initialfile=new_filename,
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if not file_path:
            return
        cv2.imwrite(file_path, self.cv_image)
        messagebox.showinfo("Info", "Image saved successfully!")

    def on_resize(self, event):
        self.display_image()


if __name__ == "__main__":
    root = ctk.CTk()
    app = FilterApp(root)
    root.mainloop()
'''