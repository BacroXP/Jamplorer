import os
from customtkinter import *
import tkinter as tk
from user import User
from file import File
from tag import Tag
import pyautogui


class Jamplorer:
    def __init__(self):
        self.active_user, self.users = self.get_users("user.dat")
        self.screen_width, self.screen_height = pyautogui.size()
        self.files = self.get_users_files()
        self.visible_files = set([self.files[file] for file in self.files])
        self.tags = self.get_users_tags()
        self.opened_file = None

        self.width = 1024
        self.height = 512

        self.app = CTk()
        self.app.geometry(f"{self.width}x{self.height}")
        set_appearance_mode("dark")
        self.app.title("Jamplorer")

        self.top_bar = None
        self.tag_bar = None
        self.search_bar = None

        self.create_top_bar(self.app)
        self.create_tag_bar(self.app)
        self.show_files(self.app)

        self.app.mainloop()

    def handle_search(self, *args):
        search_str = self.search_bar.get()

        if search_str == "":
            self.visible_files = set([self.files[file] for file in self.files])
        else:
            self.visible_files = set()
            for file in self.files:
                for i in range(len(file) // len(search_str)):
                    if file[i:i + len(search_str)] == search_str:
                        self.visible_files.add(self.files[file])

        self.show_files(self.app)

    def show_files(self, app):
        # Destroy previous files_panel if it exists
        for widget in app.winfo_children():
            if isinstance(widget, CTkFrame) and widget.winfo_name() == "!ctkframe3":
                for button in widget.winfo_children():
                    button.destroy()
                widget.destroy()

        # Create a new files_panel based on the state of opened_file
        if self.opened_file is None:
            # Full-width files_panel when no file is opened
            files_panel = CTkFrame(master=app, fg_color="#000000", corner_radius=0,
                                   width=self.screen_width, height=self.screen_height - 150)
            files_panel.place(relx=0.5, y=150, anchor="n")

            # Create buttons for visible_files within files_panel
            for i, element in enumerate(self.visible_files):
                el_button = CTkButton(master=files_panel, width=self.width - 60, height=30, corner_radius=40,
                                      text=element.get_filename(), command=lambda el=element: self.view_details(el),
                                      text_color="#00FF19", bg_color="transparent", fg_color="transparent",
                                      hover_color="#1F1F1F")
                el_button.place(relx=0.5, y=30 + (i * 35), anchor="center")
        else:
            # Half-width files_panel when a file is opened
            files_panel = CTkFrame(master=app, fg_color="#000000", corner_radius=0,
                                   width=self.screen_width // 2, height=self.screen_height - 150)
            files_panel.place(relx=0.5, y=150, anchor="ne")

            # Create buttons for visible_files within files_panel
            for i, element in enumerate(self.visible_files):
                el_button = CTkButton(master=files_panel, width=(self.width // 2) - 60, height=30, corner_radius=40,
                                      text=element.get_filename(), command=lambda el=element: self.view_details(el),
                                      text_color="#00FF19", bg_color="transparent", fg_color="transparent",
                                      hover_color="#1F1F1F")
                el_button.place(relx=0.5, x=-15, y=30 + (i * 35), anchor="w")

    def view_details(self, element):
        self.opened_file = element
        self.show_files(self.app)
        print("Viewing:", element.get_filename())

    def create_top_bar(self, app):
        self.top_bar = CTkFrame(master=app, fg_color="#1F1F1F", corner_radius=0, width=self.screen_width, height=50,
                                bg_color="transparent", border_color="#1F1F1F")
        self.top_bar.place(relx=0.5, y=0, anchor="n")

        self.create_search_bar(self.top_bar)
        self.create_accounts(self.top_bar)

    def create_tag_bar(self, app):
        self.tag_bar = CTkFrame(master=app, fg_color="#080808", corner_radius=0, width=self.screen_width, height=100,
                                bg_color="transparent", border_color="#080808")
        self.tag_bar.place(relx=0.5, y=50, anchor="n")

    def create_accounts(self, app):
        github_bubble = CTkButton(master=app, width=0, text="G", corner_radius=40, text_color="#00FF19",
                                  fg_color="#181818", border_color="#1F1F1F", hover_color="#282828")
        deepl_bubble = CTkButton(master=app, width=0, text="D", corner_radius=40, text_color="#00FF19",
                                 fg_color="#181818", border_color="#1F1F1F", hover_color="#282828")
        account_bubble = CTkButton(master=app, width=0, text="A", corner_radius=40, text_color="#00FF19",
                                   fg_color="#181818", border_color="#1F1F1F", hover_color="#282828")

        github_bubble.place(relx=0.5, x=30, rely=0.5, anchor="w")
        deepl_bubble.place(relx=0.5, x=80, rely=0.5, anchor="w")
        account_bubble.place(relx=0.5, x=130, rely=0.5, anchor="w")

    def create_search_bar(self, app):
        self.search_bar = CTkEntry(master=app, corner_radius=40, fg_color="#181818", border_color="#1F1F1F",
                                   width=self.width // 2 - 20, text_color="#00FF19")
        self.search_bar.place(relx=0.5, rely=0.5, anchor="e")
        self.search_bar.bind('<KeyRelease>', self.handle_search)

    @staticmethod
    def get_users(users_path):
        active_user = open(users_path).read().strip().split("\n")[0]
        users = {}

        for user in open(users_path).read().strip().split("\n")[1:]:
            user_data = user.split(">")
            users[user_data[0]] = User(user_data[0], user_data[1], user_data[2], user_data[3],
                                       user_data[4], user_data[5], user_data[6])

        return active_user, users

    def get_users_files(self):
        files_path = self.users[self.active_user].get_files_path()
        files = {}

        with open(files_path) as file_data:
            for line in file_data:
                line = line.strip()
                if line:
                    file_info, extra_info = line.split("?")
                    file_path, tag_data = file_info.split("-->")
                    tags = tag_data.split(",")
                    file_name = os.path.basename(file_path).split(".")[0]
                    files[file_name] = File(file_path, tags, extra_info)

        return files

    def get_users_tags(self):
        tags_path = self.users[self.active_user].get_tags_path()
        tags = {}

        with open(tags_path) as tag_data:
            for line in tag_data:
                line = line.strip()
                if line:
                    tag_path, tag_data = line.split("-->")
                    tags_name = os.path.basename(tag_path).split(".")[0]
                    tags[tags_name] = Tag(tag_path, tag_data.split(","))

        return tags
