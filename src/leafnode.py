from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict | None = None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self) -> str:
        if not self.tag:
            return self.value
        if not self.value:
            raise ValueError("Value is required for leaf node")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"