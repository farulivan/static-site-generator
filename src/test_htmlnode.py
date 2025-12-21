import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(),
            ' href="https://example.com" target="_blank"',
        )

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_constructor_fields(self):
        node = HTMLNode("a", "link text", children=["child"], props={"href": "url"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "link text")
        self.assertEqual(node.children, ["child"])
        self.assertEqual(node.props, {"href": "url"})


if __name__ == "__main__":
    unittest.main()