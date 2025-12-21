import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_no_value(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "Value cannot be empty")

    def test_leaf_value_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "Value should not be None")

    def test_leaf_multiple_props(self):
        node = LeafNode("a", "Click", {"href": "http://example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="http://example.com" target="_blank">Click</a>')

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
        
    def test_leaf_no_tag_with_props(self):
        node = LeafNode(None, "Plain text", {"class": "bold"})
        self.assertEqual(node.to_html(), "Plain text")


if __name__ == "__main__":
    unittest.main()