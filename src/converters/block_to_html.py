from typing import List
from models import HTMLNode, LeafNode, ParentNode, BlockType
from parsers.markdown import markdown_to_blocks, block_to_block_type
from .text_to_html import text_to_textnodes, text_nodes_to_html_nodes

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
