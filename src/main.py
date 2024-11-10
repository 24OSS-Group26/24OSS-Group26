import customtkinter as ctk
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
        self.root.geometry("900x750")
        ctk.set_appearance_mode("Dark")  # 다크 모드
        ctk.set_default_color_theme("blue")  # 테마 색상 설정

        self.image = None
        self.cv_image = None
        self.original_image = None  # 원본 이미지를 저장
        self.current_filter = "None"  # 현재 적용된 필터 이름 저장

        self.init_gui()

    def init_gui(self):
        # Title
        title_label = ctk.CTkLabel(self.root, text="Photo Filter Application", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=10)

        # Canvas Frame
        self.canvas_frame = ctk.CTkFrame(self.root, width=800, height=500)
        self.canvas_frame.pack(fill="both", expand=True, pady=10)
        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg="gray", bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Label for filter info
        self.filter_label = ctk.CTkLabel(self.root, text=f"Current Filter: {self.current_filter}",
                                         font=("Helvetica", 16), text_color="#00d2d3")
        self.filter_label.pack(pady=10)

        # Button frame
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10, fill=ctk.BOTH)

        # Buttons
        btn_open = ctk.CTkButton(button_frame, text="Open Image", command=self.open_image, width=120)
        btn_open.grid(row=0, column=0, padx=10, pady=10)

        btn_mosaic = ctk.CTkButton(button_frame, text="Mosaic Filter", command=self.apply_mosaic_filter, width=120)
        btn_mosaic.grid(row=0, column=1, padx=10, pady=10)

        btn_cartoon = ctk.CTkButton(button_frame, text="Cartoon Filter", command=self.apply_cartoon_filter, width=120)
        btn_cartoon.grid(row=0, column=2, padx=10, pady=10)

        btn_sketch = ctk.CTkButton(button_frame, text="Sketch Filter", command=self.apply_sketch_filter, width=120)
        btn_sketch.grid(row=0, column=3, padx=10, pady=10)

        btn_invert = ctk.CTkButton(button_frame, text="Invert Filter", command=self.apply_invert_filter, width=120)
        btn_invert.grid(row=0, column=4, padx=10, pady=10)

        btn_save = ctk.CTkButton(button_frame, text="Save Image", command=self.save_image, width=120)
        btn_save.grid(row=0, column=5, padx=10, pady=10)

        # Footer help text
        footer_label = ctk.CTkLabel(self.root, text="Tip: Open an image, apply a filter, and save it!",
                                    font=("Helvetica", 14), text_color="#bdc3c7")
        footer_label.pack(side=ctk.BOTTOM, pady=20)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if not file_path:
            return

        self.original_image = cv2.imread(file_path)  # 원본 이미지 저장
        self.cv_image = self.original_image.copy()  # 작업 이미지 초기화
        self.current_filter = "None"  # 필터 초기화
        self.update_filter_label()
        self.display_image()

    def display_image(self):
        if self.cv_image is not None:
            rgb_image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_image)

            # Get canvas dimensions
            canvas_width = self.canvas_frame.winfo_width()
            canvas_height = self.canvas_frame.winfo_height()

            # Resize image while maintaining aspect ratio
            image_ratio = image.width / image.height
            canvas_ratio = canvas_width / canvas_height

            if image_ratio > canvas_ratio:
                # Fit to canvas width
                new_width = canvas_width
                new_height = int(canvas_width / image_ratio)
            else:
                # Fit to canvas height
                new_height = canvas_height
                new_width = int(canvas_height * image_ratio)

            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            self.image = ImageTk.PhotoImage(image)
            self.canvas.delete("all")  # Clear the canvas
            self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.image)

    def update_filter_label(self):
        self.filter_label.configure(text=f"Current Filter: {self.current_filter}")

    def apply_mosaic_filter(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Open an image first!")
            return
        self.cv_image = apply_mosaic_to_faces(self.original_image.copy())
        self.current_filter = "Mosaic"
        self.update_filter_label()
        self.display_image()

    def apply_cartoon_filter(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Open an image first!")
            return
        self.cv_image = apply_cartoon_filter(self.original_image.copy())
        self.current_filter = "Cartoon"
        self.update_filter_label()
        self.display_image()

    def apply_sketch_filter(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Open an image first!")
            return
        self.cv_image = apply_sketch_filter(self.original_image.copy())
        self.current_filter = "Sketch"
        self.update_filter_label()
        self.display_image()

    def apply_invert_filter(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Open an image first!")
            return
        self.cv_image = apply_invert_filter(self.original_image.copy())
        self.current_filter = "Invert"
        self.update_filter_label()
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
    root = ctk.CTk()
    app = FilterApp(root)
    root.mainloop()
