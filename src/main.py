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
from PIL import Image, ImageTk
import numpy as np


class FilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Filter Application")
        self.root.geometry("1000x800")
        self.root.rowconfigure(2, weight=1)  # Adjust grid for filter buttons
        self.root.columnconfigure(0, weight=1)  # Center elements horizontally
        ctk.set_appearance_mode("Dark")  # Dark mode
        ctk.set_default_color_theme("blue")  # Blue theme

        self.image = None
        self.cv_image = None
        self.original_image = None  # Original image
        self.current_filter = "None"  # Name of the current filter

        self.init_gui()

    def init_gui(self):
        # Title
        title_label = ctk.CTkLabel(self.root, text="Photo Filter Application", font=("Helvetica", 28, "bold"),
                                   text_color="#1abc9c")
        title_label.grid(row=0, column=0, pady=10, sticky="n")

        # Top buttons (Open & Save)
        button_frame_top = ctk.CTkFrame(self.root, fg_color="transparent")
        button_frame_top.grid(row=1, column=0, pady=5, sticky="ew")
        button_frame_top.columnconfigure(0, weight=1)  # Open Image on the left
        button_frame_top.columnconfigure(1, weight=1)  # Spacer
        button_frame_top.columnconfigure(2, weight=1)  # Save Image on the right

        # Open Image button (left)
        btn_open = ctk.CTkButton(button_frame_top, text="Open Image", command=self.open_image, width=180,
                                 fg_color="#27ae60")
        btn_open.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        # Save Image button (right)
        btn_save = ctk.CTkButton(button_frame_top, text="Save Image", command=self.save_image, width=180,
                                 fg_color="#3498db")
        btn_save.grid(row=0, column=2, padx=15, pady=10, sticky="e")

        # Canvas Frame for displaying the image
        self.canvas_frame = ctk.CTkFrame(self.root, width=800, height=500, fg_color="transparent")
        self.canvas_frame.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg="gray", bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Label for current filter information
        self.filter_label = ctk.CTkLabel(self.root, text=f"Current Filter: {self.current_filter}",
                                         font=("Helvetica", 16), text_color="#00d2d3")
        self.filter_label.grid(row=3, column=0, pady=5, sticky="n")

        # Centralized button frame for filter buttons
        button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        button_frame.grid(row=4, column=0, pady=10, sticky="ew")
        button_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)  # Equal weight for 5 columns

        # Add buttons for each filter (3x5 layout with dynamic resizing)
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
            ("추가1", self.apply_additional_filter1),
            ("추가2", self.apply_additional_filter2),
            ("추가3", self.apply_additional_filter3),
        ]

        # Dynamically create 3 rows and 5 columns
        for i, (text, command) in enumerate(filters):
            ctk.CTkButton(button_frame, text=f"{text} Filter", command=command).grid(
                row=i // 5, column=i % 5, padx=10, pady=5, sticky="nsew"
            )

        # Footer help text
        footer_label = ctk.CTkLabel(self.root, text="Tip: Open an image, apply a filter, and save it!",
                                    font=("Helvetica", 14), text_color="#bdc3c7")
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

    # Filter methods with cancellation logic
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

    # Filter-specific methods
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

    def apply_additional_filter1(self):
        self.apply_filter(lambda img: img, "추가1")

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

        original_name = self.original_filename.split("/")[-1].split(".")[0]
        new_filename = f"{original_name}_{self.current_filter}.png"

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 initialfile=new_filename,
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if not file_path:
            return
        cv2.imwrite(file_path, self.cv_image)
        messagebox.showinfo("Info", "Image saved successfully!")


if __name__ == "__main__":
    root = ctk.CTk()
    app = FilterApp(root)
    root.mainloop()
