from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict | None = None):

        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Tag is required")
        if self.children is None:
            raise ValueError("Children should not be None")
        if not self.children:
            raise ValueError("Children cannot be empty")
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise ValueError("All children must be HTMLNode instances")
        html_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string