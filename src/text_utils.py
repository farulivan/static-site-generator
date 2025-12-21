from ast import Tuple
from textnode import TextNode, TextType
from typing import List
import re

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

def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    images_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(images_pattern, text)

def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    links_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(links_pattern, text)

def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            images = extract_markdown_images(text)
            if not images:
                new_nodes.append(node)
            else:
                current_text = text
                for alt, url in images:
                    sections = current_text.split(f"![{alt}]({url})", 1)
                    if sections[0]:  # before, non-empty
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                    current_text = sections[1] if len(sections) > 1 else ""
                if current_text:  # remaining text
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            links = extract_markdown_links(text)
            if not links:
                new_nodes.append(node)
            else:
                current_text = text
                for alt, url in links:
                    sections = current_text.split(f"[{alt}]({url})", 1)
                    if sections[0]:  # before, non-empty
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.LINK, url))
                    current_text = sections[1] if len(sections) > 1 else ""
                if current_text:  # remaining text
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes