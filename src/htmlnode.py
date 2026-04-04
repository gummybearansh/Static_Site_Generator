# represents a 'node' in an HTML document - can be blocklevel or inline


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplemented

    def props_to_html(self):
        if not self.props:
            return ""
        else:
            props_repr = ""
            for prop in self.props:
                props_repr += f' {prop}="{self.props[prop]}"'

        return props_repr

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
