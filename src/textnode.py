from enum import Enum

TextType = Enum('TextType', ['plain', 'bold', 'italic', 'code', 'links', 'images'])

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "url"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if type(other) is not TextNode:
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )


    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}({self.text}, {self.text_type.value}, {self.url})"
