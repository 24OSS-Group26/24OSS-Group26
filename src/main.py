import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from filters.mosaic import apply_mosaic_to_faces
from filters.grayscale import apply_grayscale
from filters.cartoon import apply_cartoon_filter
from filters.sketch import apply_sketch_filter
from filters.invert import apply_invert_filter
from PIL import Image, ImageTk


class FilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Filter Application")
        self.image = None
        self.cv_image = None
        self.original_image = None  # 원본 이미지를 저장

        self.init_gui()

    def init_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, fill=tk.X)

        btn_open = tk.Button(frame, text="Open Image", command=self.open_image)
        btn_open.pack(side=tk.LEFT, padx=5, pady=5)

        btn_mosaic = tk.Button(frame, text="Mosaic Filter", command=self.apply_mosaic_filter)
        btn_mosaic.pack(side=tk.LEFT, padx=5, pady=5)

        btn_cartoon = tk.Button(frame, text="Cartoon Filter", command=self.apply_cartoon_filter)
        btn_cartoon.pack(side=tk.LEFT, padx=5, pady=5)

        btn_sketch = tk.Button(frame, text="Sketch Filter", command=self.apply_sketch_filter)
        btn_sketch.pack(side=tk.LEFT, padx=5, pady=5)

        btn_invert = tk.Button(frame, text="Invert Filter", command=self.apply_invert_filter)
        btn_invert.pack(side=tk.LEFT, padx=5, pady=5)

        btn_save = tk.Button(frame, text="Save Image", command=self.save_image)
        btn_save.pack(side=tk.LEFT, padx=5, pady=5)

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if not file_path:
            return

        self.original_image = cv2.imread(file_path)  # 원본 이미지 저장
        self.cv_image = self.original_image.copy()  # 작업 이미지 초기화
        self.display_image()

    def display_image(self):
        if self.cv_image is not None:
            rgb_image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_image)
            image.thumbnail((600, 400))
            self.image = ImageTk.PhotoImage(image)
            self.canvas.create_image(300, 200, image=self.image)

    def apply_mosaic_filter(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Open an image first!")
            return
        self.cv_image = apply_mosaic_to_faces(self.original_image.copy())
        self.display_image()

    def apply_cartoon_filter(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Open an image first!")
            return
        self.cv_image = apply_cartoon_filter(self.original_image.copy())
        self.display_image()

    def apply_sketch_filter(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Open an image first!")
            return
        self.cv_image = apply_sketch_filter(self.original_image.copy())
        self.display_image()

    def apply_invert_filter(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Open an image first!")
            return
        self.cv_image = apply_invert_filter(self.original_image.copy())
        self.display_image()

    def save_image(self):
        if self.cv_image is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if not file_path:
            return
        cv2.imwrite(file_path, self.cv_image)
        messagebox.showinfo("Info", "Image saved successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = FilterApp(root)
    root.mainloop()
