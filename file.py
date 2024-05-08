import os
from tkinter import messagebox
import tkinter as tk


class File:
    def __init__(self, path, tags, i):
        self.path = path
        self.tags = tags
        self.index = i
        self.filename = os.path.basename(path).split(".")[0]
        self.filetype = path.split(".")[-1].lower()

        print(f"Saved/Restored the file {self.filename} with the tags {', '.join(map(str, self.tags))}.")

    def display_filename(self, file_viewer):
        filename_label = tk.Label(file_viewer, text=self.filename, font=("Helvetica", 16))
        filename_label.pack(pady=10)

        filename_label.configure(bg=file_viewer.cget('bg'))

    def display_options(self, file_viewer):
        # Frame to hold buttons
        button_frame = tk.Frame(file_viewer)
        button_frame.pack(pady=10)

        # Create additional buttons
        upload_button = tk.Button(button_frame, text="Upload", command=self.upload_file())
        upload_button.pack(side=tk.LEFT, padx=10)

        # Open button
        open_button = tk.Button(button_frame, text="Open File", command=self.open_file)
        open_button.pack(padx=10)

        button_frame.configure(bg=file_viewer.cget('bg'))

    def upload_file(self):
        pass

    def get_filename(self):
        return self.filename

    def get_filetype(self):
        return self.filetype

    def get_filepath(self):
        return self.path

    def open_file(self):
        try:
            os.startfile(self.path)
        except OSError as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")
