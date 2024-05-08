
class Tag:
    def __init__(self, name, tags, i):
        self.name = name
        self.sub_tags = tags
        self.index = i

        print(f"Saved/Restored the tag {self.name} with the sub_tags {', '.join(map(str, self.sub_tags))}.")

    def get_sub_tags(self):
        return self.sub_tags

    def remove_tag(self):
        del self
