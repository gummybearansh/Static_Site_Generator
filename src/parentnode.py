from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None: 
            raise ValueError("Parent Node needs to have a tag")

        if self.children is None:
            raise ValueError("Parent node must have children")

        # if it's a leaf node - i can just call to_html on it and it'll include the closing tag as well
        # same for parent node - recursively calling to_html will make sure all it's children are formatted in proper string as well
        children_string = ''
        for child in self.children: 
            children_string += child.to_html()

        return f'<{self.tag}>{self.props_to_html()}{children_string}</{self.tag}>'

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

