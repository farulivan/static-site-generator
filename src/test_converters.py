import unittest
from converters import markdown_to_blocks, text_node_to_html_node, text_to_textnodes, block_to_block_type
from textnode import TextNode
from enums import BlockType, TextType

class TestConverters(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_text_node_to_html_node_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_text_node_to_html_node_code(self):
        node = TextNode("code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code text")

    def test_text_node_to_html_node_link(self):
        node = TextNode("link text", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "link text")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_node_to_html_node_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "alt text"})

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_markdown_to_blocks_single_block(self):
        self.assertEqual(markdown_to_blocks("Single block"), ["Single block"])

    def test_markdown_to_blocks_with_empty_blocks(self):
        md = "\n\n\n\nBlock\n\n\n\n"
        self.assertEqual(markdown_to_blocks(md), ["Block"])

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        md = "  \n\n  Block  \n\n  "
        self.assertEqual(markdown_to_blocks(md), ["Block"])

    def test_markdown_to_blocks_only_newlines(self):
        self.assertEqual(markdown_to_blocks("\n\n\n"), [])

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        self.assertEqual(block_to_block_type("> quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> line1\n> line2"), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- item1\n- item2"), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. item1\n2. item2\n3. item3"), BlockType.ORDERED_LIST)
        # Invalid: not starting from 1
        self.assertEqual(block_to_block_type("2. item"), BlockType.PARAGRAPH)
        # Invalid: not sequential
        self.assertEqual(block_to_block_type("1. item\n3. item"), BlockType.PARAGRAPH)
        # Invalid: not numbers
        self.assertEqual(block_to_block_type("a. item"), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(block_to_block_type("Plain text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Text\nMore text"), BlockType.PARAGRAPH)
        # Heading without space
        self.assertEqual(block_to_block_type("#No space"), BlockType.PARAGRAPH)
        # Code not starting/ending
        self.assertEqual(block_to_block_type("```code"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()