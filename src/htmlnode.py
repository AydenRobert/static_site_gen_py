import re


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        return " ".join(map(lambda x: f'{x[0]}="{x[1]}"', self.props.items()))

    def __repr__(self):
        return f"HTMLNode(\n{self.tag},\n{self.value},\n{self.children},\n{self.props}\n)"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("All leaf nodes must have a value")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        props_str = " " + self.props_to_html() if self.props is not None else ""
        return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if children is None:
            raise ValueError("All parent nodes must have children")
        if tag is None:
            raise ValueError("All parent nodes must have a tag")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children is None:
            raise ValueError("All parent nodes must have children")
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")

        string_list = "".join(map(lambda x: x.to_html(), self.children))
        props_str = " " + self.props_to_html() if self.props is not None else ""
        return f'<{self.tag}{props_str}>{string_list}</{self.tag}>'


class PNode(HTMLNode):
    def __init__(self, value, children=None, props=None):
        children = list()
        super().__init__("p", value, children, props)

    def to_html(self):
        props_str = " " + self.props_to_html() if self.props is not None else ""
        value_str = ""
        replacements = iter(self.children)
        if self.value is not None:
            value_str = re.sub(
                r"\{\}",                     # match literal "{}"
                lambda match: next(replacements).to_html(),
                self.value
            )
        return f'<{self.tag}{props_str}>{value_str}</{self.tag}>'

    def append(self, node):
        self.children.append(node)


class NoneNode(HTMLNode):
    def __init__(self, value, children=None):
        children = list()
        super().__init__(None, value, children, None)

    def to_html(self):
        value_str = ""
        replacements = iter(self.children)
        if self.value is not None:
            value_str = re.sub(
                r"\{\}",                     # match literal "{}"
                lambda match: next(replacements).to_html(),
                self.value
            )
        return f'{value_str}'

    def append(self, node):
        self.children.append(node)
