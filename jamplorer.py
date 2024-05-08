from file import File
from tag import Tag
from pics import Pic
from customtkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import math


class Jamplorer:
    def __init__(self):
        self.files = set()
        self.tags = set()
        self.root = tk.Tk()
        self.root.title("Jamplorer")
        self.width = 800
        self.height = 600
        self.root.geometry(f"{self.width}x{self.height}")
        self.paned_window = None
        self.file_list_frame = None
        self.file_viewer = None
        self.start_x = self.width * 0.66
        self.load_files()
        self.load_tags()
        self.create_window()
        self.search_var = ""
        self.search_entry = None

    def add_tag(self, name, sub_tags):
        self.tags.add(Tag(name, sub_tags, len(self.tags)))

        lines = [f"{t.name}-->{','.join(t.sub_tags)}" for t in self.tags]
        with open("tags.dat", "w") as file:
            file.write("\n".join(lines))

    def remove_tag(self, name):
        for tag in self.tags:
            if tag.name == name:
                confirm = messagebox.askyesno("Confirmation", f"Are you sure you want to delete the tag '{name}'?")
                if confirm:
                    tag.remove_tag()
                    self.tags.remove(tag)

                    lines = [f"{t.name}-->{','.join(t.sub_tags)}" for t in self.tags]
                    with open("tags.dat", "w") as file:
                        file.write("\n".join(lines))
                    print(f"Tag '{name}' deleted successfully.")

                    break

    def handle_search(self, *args):
        search_query = self.search_var.get()
        displayable_files = []

        if len(search_query) != 0:
            for f, file_name in enumerate([file.filename for file in self.files]):
                for i in range(math.ceil(len(file_name) / len(search_query))):
                    if file_name[i: i + len(search_query)] == search_query:
                        displayable_files.append(self.files[f])
        else:
            displayable_files = self.files

        self.display_files(displayable_files)

    def create_window(self):
        # Create a PanedWindow to hold left and right panes
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=5, sashpad=5, sashrelief=tk.RAISED)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.create_left_pane()
        self.create_right_pane()

        # Create a separator (sash) between the panes
        self.paned_window.sash_place(0, 400, 1)  # Set initial position of the sash (splitter)

        # Bind mouse events to allow resizing with the sash
        self.paned_window.bind("<Button-1>", self.start_resize)
        self.paned_window.bind("<B1-Motion>", self.resize)

        # Start the main event loop
        self.root.mainloop()

    def create_left_pane(self):
        # Left pane (file list)
        self.file_list_frame = tk.Frame(self.paned_window, bg="gray")
        self.file_list_frame.pack(fill=tk.BOTH, expand=True)
        self.paned_window.add(self.file_list_frame)

        # Searchbar
        self.create_search_bar()

        # Import button
        import_button = tk.Button(self.file_list_frame, text="Import new Content", command=self.import_file)
        import_button.pack(pady=5)

    def create_right_pane(self):
        self.file_viewer = tk.Frame(self.paned_window, bg="lightgray")
        self.file_viewer.pack(fill=tk.BOTH, expand=True)
        self.paned_window.add(self.file_viewer)

    def create_search_bar(self):
        # Create a search bar (entry widget)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.file_list_frame, textvariable=self.search_var)
        self.search_entry.pack(pady=10, padx=10, fill=tk.X)

        # Bind a callback function to handle search events (e.g., typing in the search bar)
        self.search_var.trace_add("write", self.handle_search)
        self.display_files(self.files)

    def display_files(self, searched_files):
        # Delete displayed file list
        for widget in self.file_list_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        # Display file list
        for file in searched_files:
            file_button = tk.Button(self.file_list_frame, text=file.get_filename(),
                                    command=lambda f=file: self.display_file_details(f))
            file_button.pack(pady=5)

    def display_file_details(self, file):
        for widget in self.file_viewer.winfo_children():
            widget.destroy()

        file.display_filename(self.file_viewer)

        if isinstance(file, Pic):
            file.display_pic_info(self.file_viewer.winfo_width() - 20, self.file_viewer.winfo_height() - 100, self.file_viewer)

        file.display_options(self.file_viewer)

    def import_file(self):
        # Let the user decide which file or files to import into the system
        file_paths = filedialog.askopenfilenames(
            initialdir="/",  # Initial directory (optional)
            title="Select File(s) to Import",
            filetypes=(("All Files", "*.*"), ("PNG Files", "*.png"), ("JPEG Files", "*.jpg"))
        )

        if file_paths:
            for file_path in file_paths:
                if file_path.endswith((".png", ".jpg", ".jpeg")):
                    self.files.add(Pic(file_path, tags=[], i=len(self.files)))
                else:
                    self.files.add(File(file_path, tags=[], i=len(self.files)))
            self.add_file()
            self.display_files(self.files)

    def add_file(self):
        lines = [f"{f.filename}-->{','.join(f.tags)}" for f in self.files]
        with open("tags.dat", "w") as file:
            file.write("\n".join(lines))

    def start_resize(self, event):
        self.start_x = event.x

    def resize(self, event):
        delta_x = event.x - self.start_x
        self.paned_window.sash_place(0, int(self.paned_window.sash_coord(0)[0] + delta_x), 1)
        self.start_x = event.x

    def load_tags(self):
        for i, line in enumerate(open("tags.dat").read().strip().split("\n")):
            tag_name, sub_tags = line.split("-->")
            sub_tags = sub_tags.split(",")
            self.tags.add(Tag(tag_name, sub_tags, i))

    def load_files(self):
        for i, line in enumerate(open("files.dat").read().strip().split("\n")):
            file_path, tags = line.split("-->")
            tags = tags.split(",")
            if file_path.split(".")[-1].lower() in ["png", "jpg", "jpeg"]:
                self.files.add(Pic(file_path, tags, i))
            else:
                self.files.add(File(file_path, tags, i))
