import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_split = node.text.split(delimiter)

        # don't hardcode it to 3 -> string can have multiple delimiter sections
        if len(node_split) % 2 == 0: 
            raise SyntaxError("Invalid Markdown Syntax")

        this_node = []
        for i in range(len(node_split)):
            # spliting but starting contains `code` then the starting string will be empty
            if node_split[i] == "":
                continue
            if i % 2 != 0:
                this_node.append(TextNode(node_split[i], text_type))
            else: 
                this_node.append(TextNode(node_split[i], TextType.TEXT))

        new_nodes.extend(this_node)

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_images(old_nodes):
    pass

