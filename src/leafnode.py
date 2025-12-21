from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict | None = None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self) -> str:
        if not self.tag:
            return self.value
        if self.value is None:
            raise ValueError("Value should not be None")
        if not self.value:
            raise ValueError("Value cannot be empty")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"