import unittest
from text_utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode
from enums import TextType

class TestTextUtils(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This is `code` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_only_delimited(self):
        node = TextNode("`code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("code", TextType.CODE)]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_multiple_regions(self):
        node = TextNode("This `one` and `two`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("one", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.CODE)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_invalid(self):
        node = TextNode("This `broken", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_delimiter_non_text_passed(self):
        nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode("This is `code`", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_empty_parts(self):
        node = TextNode("**a****b**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("a", TextType.BOLD),
            TextNode("b", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![img1](url1) and ![img2](url2)"
        )
        self.assertListEqual([("img1", "url1"), ("img2", "url2")], matches)

    def test_extract_markdown_images_with_text(self):
        matches = extract_markdown_images(
            "Here is ![an image](https://example.com/img.png) in text"
        )
        self.assertListEqual([("an image", "https://example.com/img.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "[link1](url1) and [link2](url2)"
        )
        self.assertListEqual([("link1", "url1"), ("link2", "url2")], matches)

    def test_split_nodes_image_basic(self):
        node = TextNode("This is ![alt](url)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_no_images(self):
        node = TextNode("Plain text", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [TextNode("Plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple(self):
        node = TextNode("![img1](url1) and ![img2](url2)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_with_text(self):
        node = TextNode("Before ![alt](url) after", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" after", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_non_text(self):
        nodes = [TextNode("bold", TextType.BOLD)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, nodes)

    def test_split_nodes_link_basic(self):
        node = TextNode("This is [text](url)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.LINK, "url")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_no_links(self):
        node = TextNode("Plain text", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("Plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_link_multiple(self):
        node = TextNode("[link1](url1) and [link2](url2)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_with_text(self):
        node = TextNode("Before [text](url) after", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("text", TextType.LINK, "url"),
            TextNode(" after", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple_nodes(self):
        nodes = [TextNode("a ![x](u)", TextType.TEXT), TextNode(" and ![y](v)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("x", TextType.IMAGE, "u"),
            TextNode(" and ", TextType.TEXT),
            TextNode("y", TextType.IMAGE, "v")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_at_start(self):
        node = TextNode("![only](url) text", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("only", TextType.IMAGE, "url"),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_at_end(self):
        node = TextNode("text ![end](url)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "url")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_only_image(self):
        node = TextNode("![only](url)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [TextNode("only", TextType.IMAGE, "url")]
        self.assertEqual(result, expected)

    def test_split_nodes_image_empty_alt(self):
        node = TextNode("![](url)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [TextNode("", TextType.IMAGE, "url")]
        self.assertEqual(result, expected)

    def test_split_nodes_image_and_link_interaction_complex(self):
        # Test multiple interleaved images and links
        node = TextNode("![a](u1) and [l1](v1) then ![b](u2) and [l2](v2)", TextType.TEXT)
        after_image = split_nodes_image([node])
        result = split_nodes_link(after_image)
        expected = [
            TextNode("a", TextType.IMAGE, "u1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("l1", TextType.LINK, "v1"),
            TextNode(" then ", TextType.TEXT),
            TextNode("b", TextType.IMAGE, "u2"),
            TextNode(" and ", TextType.TEXT),
            TextNode("l2", TextType.LINK, "v2")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_multiple_nodes(self):
        nodes = [TextNode("a [x](u)", TextType.TEXT), TextNode(" and [y](v)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("x", TextType.LINK, "u"),
            TextNode(" and ", TextType.TEXT),
            TextNode("y", TextType.LINK, "v")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_at_start(self):
        node = TextNode("[only](url) text", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("only", TextType.LINK, "url"),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_at_end(self):
        node = TextNode("text [end](url)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("end", TextType.LINK, "url")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_only_link(self):
        node = TextNode("[only](url)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("only", TextType.LINK, "url")]
        self.assertEqual(result, expected)

    def test_split_nodes_link_empty_alt(self):
        node = TextNode("[](url)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("", TextType.LINK, "url")]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()