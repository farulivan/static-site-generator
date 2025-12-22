from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
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

def text_nodes_to_html_nodes(text_nodes: List[TextNode]) -> List[HTMLNode]:
    return [text_node_to_html_node(node) for node in text_nodes]

def paragraph_block_to_html_node(block: str) -> HTMLNode:
    block = block.replace('\n', ' ')
    text_nodes = text_to_textnodes(block)
    html_nodes = text_nodes_to_html_nodes(text_nodes)
    return ParentNode("p", html_nodes)

def heading_block_to_html_node(block: str) -> HTMLNode:
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    text = block[level:].strip()
    text_nodes = text_to_textnodes(text)
    html_nodes = text_nodes_to_html_nodes(text_nodes)
    return ParentNode(f"h{level}", html_nodes)

def code_block_to_html_node(block: str) -> HTMLNode:
    lines = block.split('\n')
    content = '\n'.join(lines[1:-1])
    if content:
        content += '\n'
    code_node = LeafNode("code", content)
    return ParentNode("pre", [code_node])

def quote_block_to_html_node(block: str) -> HTMLNode:
    lines = block.split('\n')
    quote_text = '\n'.join(line.lstrip('> ').lstrip('>').strip() for line in lines)
    quote_text = quote_text.replace('\n', ' ')
    text_nodes = text_to_textnodes(quote_text)
    html_nodes = text_nodes_to_html_nodes(text_nodes)
    return ParentNode("blockquote", html_nodes)

def unordered_list_block_to_html_node(block: str) -> HTMLNode:
    lines = block.split('\n')
    li_nodes = []
    for line in lines:
        item_text = line.lstrip('- ').strip()
        text_nodes = text_to_textnodes(item_text)
        html_nodes = text_nodes_to_html_nodes(text_nodes)
        li_nodes.append(ParentNode("li", html_nodes))
    return ParentNode("ul", li_nodes)

def ordered_list_block_to_html_node(block: str) -> HTMLNode:
    lines = block.split('\n')
    li_nodes = []
    for line in lines:
        idx = line.find('. ')
        if idx != -1:
            item_text = line[idx+2:].strip()
            text_nodes = text_to_textnodes(item_text)
            html_nodes = text_nodes_to_html_nodes(text_nodes)
            li_nodes.append(ParentNode("li", html_nodes))
    return ParentNode("ol", li_nodes)

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_block_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_block_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_block_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_block_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_block_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_block_to_html_node(block))
    return ParentNode("div", children)
