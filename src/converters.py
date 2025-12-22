from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from text_utils import split_nodes_delimiter, split_nodes_image, split_nodes_link
from enums import BlockType, TextType
import re

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")

def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown: str) -> List[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]

def block_to_block_type(single_markdown_block: str) -> BlockType:
    lines = single_markdown_block.split('\n')
    
    # Heading: starts with 1-6 # followed by space
    if re.match(r'^#{1,6} ', lines[0]):
        return BlockType.HEADING
    
    # Code block: starts and ends with ```
    if single_markdown_block.startswith('```') and single_markdown_block.endswith('```'):
        return BlockType.CODE
    
    # Quote: every line starts with >
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    # Unordered list: every line starts with - followed by space
    if all(re.match(r'^- ', line) for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Ordered list: every line starts with number. space, numbers 1,2,3,...
    if all(re.match(r'^\d+\. ', line) for line in lines):
        numbers = []
        for line in lines:
            match = re.match(r'^(\d+)\. ', line)
            numbers.append(int(match.group(1)))
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST
    
    # Default: paragraph
    return BlockType.PARAGRAPH