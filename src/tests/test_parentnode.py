import unittest
from models import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multiple_children(self):
        child1 = LeafNode("b", "bold")
        child2 = LeafNode(None, "normal")
        child3 = LeafNode("i", "italic")
        parent = ParentNode("p", [child1, child2, child3])
        self.assertEqual(parent.to_html(), "<p><b>bold</b>normal<i>italic</i></p>")

    def test_with_props(self):
        child = LeafNode("span", "content")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        self.assertEqual(parent.to_html(), '<div class="container" id="main"><span>content</span></div>')

    def test_tag_none(self):
        with self.assertRaises(ValueError) as cm:
            node = ParentNode(None, [LeafNode("p", "test")])
            node.to_html()
        self.assertEqual(str(cm.exception), "Tag is required")

    def test_children_none(self):
        with self.assertRaises(ValueError) as cm:
            node = ParentNode("div", None)
            node.to_html()
        self.assertEqual(str(cm.exception), "Children should not be None")

    def test_empty_children(self):
        with self.assertRaises(ValueError) as cm:
            node = ParentNode("div", [])
            node.to_html()
        self.assertEqual(str(cm.exception), "Children cannot be empty")

    def test_invalid_child_type(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode("div", ["not a node"]).to_html()
        self.assertEqual(str(cm.exception), "All children must be HTMLNode instances")

    def test_deep_nesting(self):
        leaf = LeafNode("b", "deep")
        parent1 = ParentNode("span", [leaf])
        parent2 = ParentNode("div", [parent1])
        parent3 = ParentNode("section", [parent2])
        parent4 = ParentNode("article", [parent3])
        self.assertEqual(
            parent4.to_html(),
            "<article><section><div><span><b>deep</b></span></div></section></article>",
        )

if __name__ == "__main__":
    unittest.main()
