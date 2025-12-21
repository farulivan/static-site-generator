import unittest
from text_utils import split_nodes_delimiter
from textnode import TextNode, TextType

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


if __name__ == "__main__":
    unittest.main()