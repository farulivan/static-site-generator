from typing import List
from models import BlockType
import re

def markdown_to_blocks(markdown: str) -> List[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]

def block_to_block_type(single_markdown_block: str) -> BlockType:
    lines = single_markdown_block.split('\n')
    
    if re.match(r'^#{1,6} ', lines[0]):
        return BlockType.HEADING
    
    if single_markdown_block.startswith('```') and single_markdown_block.endswith('```'):
        return BlockType.CODE
    
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    if all(re.match(r'^- ', line) for line in lines):
        return BlockType.UNORDERED_LIST
    
    if all(re.match(r'^\d+\. ', line) for line in lines):
        numbers = []
        for line in lines:
            match = re.match(r'^(\d+)\. ', line)
            numbers.append(int(match.group(1)))
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def extract_title(markdown: str) -> str:
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    raise ValueError("No h1 header found")
