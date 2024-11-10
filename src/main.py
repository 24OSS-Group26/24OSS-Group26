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
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        title_label = tk.Label(main_frame, text="Photo Filter Application", bg="#34495e", fg="white",
                               font=("Helvetica", 16, "bold"), pady=10)
        title_label.pack(fill=tk.X)

        # Canvas for image display
        self.canvas = tk.Canvas(main_frame, width=800, height=500, bg="#ecf0f1", bd=0, highlightthickness=0)
        self.canvas.pack(pady=10)

        # Button frame
        button_frame = tk.Frame(main_frame, bg="#2c3e50")
        button_frame.pack(fill=tk.X, pady=10)

        # Button styles
        button_style = {"bg": "#2980b9", "fg": "white", "font": ("Helvetica", 12), "width": 15, "relief": "raised"}

        # Buttons
        btn_open = tk.Button(button_frame, text="Open Image", command=self.open_image, **button_style)
        btn_open.pack(side=tk.LEFT, padx=5, pady=5)

        btn_mosaic = tk.Button(button_frame, text="Mosaic Filter", command=self.apply_mosaic_filter, **button_style)
        btn_mosaic.pack(side=tk.LEFT, padx=5, pady=5)

        btn_cartoon = tk.Button(button_frame, text="Cartoon Filter", command=self.apply_cartoon_filter, **button_style)
        btn_cartoon.pack(side=tk.LEFT, padx=5, pady=5)

        btn_sketch = tk.Button(button_frame, text="Sketch Filter", command=self.apply_sketch_filter, **button_style)
        btn_sketch.pack(side=tk.LEFT, padx=5, pady=5)

        btn_invert = tk.Button(button_frame, text="Invert Filter", command=self.apply_invert_filter, **button_style)
        btn_invert.pack(side=tk.LEFT, padx=5, pady=5)

        btn_save = tk.Button(button_frame, text="Save Image", command=self.save_image, **button_style)
        btn_save.pack(side=tk.LEFT, padx=5, pady=5)

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
            image.thumbnail((800, 500))
            self.image = ImageTk.PhotoImage(image)
            self.canvas.create_image(400, 250, image=self.image)

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
