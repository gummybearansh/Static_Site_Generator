# represents the inline text possible in HTML and Markdown
from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        # making text_type an enum (passed as a string while creation but type will be : <'enum': 'TextType'>
        self.text_type = TextType(text_type)
        self.url = url

    # comparing two TextNodes to be equal if:
    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    # string representation of TextNode (when printing)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
