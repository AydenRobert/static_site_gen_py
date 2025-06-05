import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "string")
        expected_result = "HTMLNode(\nh1,\nstring,\nNone,\nNone\n)"
        self.assertEqual(node.__repr__(), expected_result)

    def test_props(self):
        node = HTMLNode(
            props={"href": "https://www.youtube.com", "target": "_blank"})
        expected_result = 'href="https://www.youtube.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_result)

    def test_not_implemented(self):
        node = HTMLNode(value="something")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_val_err(self):
        with self.assertRaises(ValueError):
            LeafNode("p")

    def test_leaf_no_tag(self):
        node = LeafNode(value="somebody once told me")
        self.assertEqual(node.to_html(), "somebody once told me")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
