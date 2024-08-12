import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk


# Function to perform pixel manipulation for encryption/decryption
def manipulate_pixel(value, key):
    return (value + key) % 256


# Encrypt or decrypt an image
def process_image(image, key, is_encrypting=True):
    pixels = image.load()
    width, height = image.size

    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            if is_encrypting:
                r = manipulate_pixel(r, key)
                g = manipulate_pixel(g, key)
                b = manipulate_pixel(b, key)
            else:
                r = manipulate_pixel(r, -key)
                g = manipulate_pixel(g, -key)
                b = manipulate_pixel(b, -key)
            pixels[x, y] = (r, g, b)

    return image


# GUI for the image encryption tool
class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        self.original_image = None
        self.processed_image = None

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Welcome to Image Encryption Tool", font=("Helvetica", 16), bg="#f0f0f0")
        self.label.pack(pady=10)

        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image, bg="#2196F3", fg="white")
        self.load_button.pack(pady=5)

        self.encrypt_button = tk.Button(self.root, text="Encrypt Image", command=self.encrypt_image, bg="#4CAF50",
                                        fg="white")
        self.encrypt_button.pack(pady=5)

        self.decrypt_button = tk.Button(self.root, text="Decrypt Image", command=self.decrypt_image, bg="#F44336",
                                        fg="white")
        self.decrypt_button.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Save Processed Image", command=self.save_image, bg="#FFC107",
                                     fg="black")
        self.save_button.pack(pady=5)

        self.compare_button = tk.Button(self.root, text="Compare Images", command=self.compare_images, bg="#9C27B0",
                                        fg="white")
        self.compare_button.pack(pady=5)

        self.preview_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.preview_frame.pack(pady=10)

        self.original_img_label = tk.Label(self.preview_frame, text="Original Image")
        self.original_img_label.grid(row=0, column=0, padx=5)
        self.processed_img_label = tk.Label(self.preview_frame, text="Processed Image")
        self.processed_img_label.grid(row=0, column=1, padx=5)

        self.original_img_canvas = tk.Canvas(self.preview_frame, width=300, height=300, bg="#e0e0e0")
        self.original_img_canvas.grid(row=1, column=0, padx=5, pady=5)
        self.processed_img_canvas = tk.Canvas(self.preview_frame, width=300, height=300, bg="#e0e0e0")
        self.processed_img_canvas.grid(row=1, column=1, padx=5, pady=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Select Image File",
                                               filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if not file_path:
            return

        self.original_image = Image.open(file_path)
        self.display_image(self.original_image, self.original_img_canvas)

    def encrypt_image(self):
        self.process_image_and_display(is_encrypting=True)

    def decrypt_image(self):
        self.process_image_and_display(is_encrypting=False)

    def process_image_and_display(self, is_encrypting):
        if not self.original_image:
            messagebox.showwarning("Warning", "No image loaded!")
            return

        key = simpledialog.askinteger("Encryption Key", "Enter a key (integer between 0 and 255):", minvalue=0,
                                      maxvalue=255)
        if key is None:
            return

        self.processed_image = process_image(self.original_image.copy(), key, is_encrypting)
        self.display_image(self.processed_image, self.processed_img_canvas)

    def display_image(self, image, canvas):
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo

    def compare_images(self):
        if not self.original_image or not self.processed_image:
            messagebox.showwarning("Warning", "Both original and processed images are required for comparison!")
            return

        self.display_image(self.original_image, self.original_img_canvas)
        self.display_image(self.processed_image, self.processed_img_canvas)

    def save_image(self):
        if not self.processed_image:
            messagebox.showwarning("Warning", "No processed image to save!")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg;*.jpeg")],
                                                 title="Save Processed Image")
        if save_path:
            self.processed_image.save(save_path)
            messagebox.showinfo("Success", "Image Saved Successfully!")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()
