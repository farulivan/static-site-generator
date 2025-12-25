import unittest
from converters import (
    markdown_to_html_node,
    text_node_to_html_node,
    text_to_textnodes,
    paragraph_block_to_html_node,
    heading_block_to_html_node,
    code_block_to_html_node,
    quote_block_to_html_node,
    unordered_list_block_to_html_node,
    ordered_list_block_to_html_node,
)
from parsers import markdown_to_blocks, block_to_block_type, extract_title
from models import TextNode, BlockType, TextType

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
        self.assertEqual(block_to_block_type("2. item"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. item\n3. item"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("a. item"), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(block_to_block_type("Plain text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Text\nMore text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#No space"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```code"), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_quotes(self):
        md = """
> This is a quote
> with multiple lines
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item
3. Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_combined(self):
        md = """
# Title

This is a paragraph with **bold** text.

- List item 1
- List item 2

```
code block
```

> Quote here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Title</h1><p>This is a paragraph with <b>bold</b> text.</p><ul><li>List item 1</li><li>List item 2</li></ul><pre><code>code block\n</code></pre><blockquote>Quote here</blockquote></div>"
        self.assertEqual(html, expected)

    def test_paragraph_block_to_html_node(self):
        block = "This is **bold** text."
        node = paragraph_block_to_html_node(block)
        html = node.to_html()
        self.assertEqual(html, "<p>This is <b>bold</b> text.</p>")

    def test_heading_block_to_html_node(self):
        block = "## Heading"
        node = heading_block_to_html_node(block)
        html = node.to_html()
        self.assertEqual(html, "<h2>Heading</h2>")

    def test_code_block_to_html_node(self):
        block = "```\ncode\n```"
        node = code_block_to_html_node(block)
        html = node.to_html()
        self.assertEqual(html, "<pre><code>code\n</code></pre>")

    def test_quote_block_to_html_node(self):
        block = "> This is a quote"
        node = quote_block_to_html_node(block)
        html = node.to_html()
        self.assertEqual(html, "<blockquote>This is a quote</blockquote>")

    def test_unordered_list_block_to_html_node(self):
        block = "- Item 1\n- Item 2"
        node = unordered_list_block_to_html_node(block)
        html = node.to_html()
        self.assertEqual(html, "<ul><li>Item 1</li><li>Item 2</li></ul>")

    def test_ordered_list_block_to_html_node(self):
        block = "1. First\n2. Second"
        node = ordered_list_block_to_html_node(block)
        html = node.to_html()
        self.assertEqual(html, "<ol><li>First</li><li>Second</li></ol>")

    def test_extract_title_simple(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    def test_extract_title_with_spaces(self):
        md = "#  Hello World  "
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_not_first_line(self):
        md = "\n\n# Title\n"
        self.assertEqual(extract_title(md), "Title")

    def test_extract_title_no_h1(self):
        md = "## Subtitle\nNo h1"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_empty_after_hash(self):
        md = "#"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_no_space(self):
        md = "#Hello"
        with self.assertRaises(ValueError):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
