class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None,
                 children: list | None = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self) -> str:
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        if not self.props:
            return ""
        list_of_props = []
        for key, value in self.props.items():
            list_of_props.append(f'{key}="{value}"')
        return " " + " ".join(list_of_props)
