from textnode import TextNode, TextType
from typing import List

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError(f"Invalid markdown syntax: unmatched delimiter '{delimiter}' in text '{node.text}'")
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part:  # non-empty text
                        new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    if part:  # non-empty delimited text
                        new_nodes.append(TextNode(part, text_type))
    return new_nodes