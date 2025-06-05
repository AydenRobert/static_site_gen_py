import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("Url will be set to none", TextType.LINK)
        node2 = TextNode("Url will be set to none", TextType.LINK, None)
        self.assertEqual(node, node2)

    def test_not_eq_str(self):
        node = TextNode("string 1", TextType.NORMAL_TEXT)
        node2 = TextNode("string 2", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("string", TextType.NORMAL_TEXT)
        node2 = TextNode("string", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_stringify(self):
        node = TextNode("string", TextType.NORMAL_TEXT)
        expected_text = "TextNode(string, TextType.NORMAL_TEXT, None)"
        self.assertEqual(f"{node}", expected_text)


if __name__ == "__main__":
    unittest.main()
