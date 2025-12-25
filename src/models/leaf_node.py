from .html_node import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict | None = None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.tag is None:
            return self.value
        if self.value is None or self.value == "":
            if self.tag not in ['img', 'br', 'hr', 'input', 'meta']:
                raise ValueError("Value cannot be empty")
        attrs = ""
        if self.props:
            attrs = " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())
        if self.tag in ['img', 'br', 'hr', 'input', 'meta']:
            return f"<{self.tag}{attrs}>"
        else:
            return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"
