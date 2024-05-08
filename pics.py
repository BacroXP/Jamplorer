from file import File  # Assuming File class is defined in file.py
from PIL import Image, ImageTk
import tkinter as tk


class Pic(File):
    def __init__(self, path, tags, i):
        super().__init__(path, tags, i)  # Correctly call parent constructor using super()
        self.picture = Image.open(path)

    def display_pic_info(self, width, height, file_viewer):
        resized_image = self.picture.resize((width, height))  # Resize the image
        tk_image = ImageTk.PhotoImage(resized_image)

        # Create or update the image label in the file_viewer widget
        if hasattr(file_viewer, 'image_label'):
            file_viewer.image_label.configure(image=tk_image)
            file_viewer.image_label.image = tk_image  # Keep a reference to the image to prevent garbage collection
        else:
            file_viewer.image_label = tk.Label(file_viewer, image=tk_image)
            file_viewer.image_label.pack(pady=10)

        # Bind a function to update image size on window resize
        file_viewer.bind("<Configure>", lambda event: self.update_image_size(event, self, file_viewer))

    @staticmethod
    def update_image_size(event, pic, file_viewer):
        # Get the new size of the window
        width = event.width - 20

        w, h = pic.picture.size
        ratio = h / w

        height = int(width * ratio)

        # Display the resized image
        pic.display_pic_info(width, height, file_viewer)
