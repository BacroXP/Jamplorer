
class User:
    def __init__(self, name, language, files_path, tags_path, hide, history, colors):
        self.name = name
        self.language = language
        self.files_path = files_path
        self.tags_path = tags_path
        self.hide = hide
        self.history = history
        self.colors = [color for color in colors.split(",")]

    def get_files_path(self):
        return self.files_path

    def get_tags_path(self):
        return self.tags_path

    def get_name(self):
        return self.name

    def get_initials(self):
        return self.get_name()[:1]
