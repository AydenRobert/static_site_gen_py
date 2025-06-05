import unittest

from textnode import TextNode, TextType
from splitnodes import *


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_simple_bold(self):
        nodes = [TextNode("This is **bold** text", TextType.NORMAL_TEXT)]
        expected = [
            TextNode("This is ", TextType.NORMAL_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" text", TextType.NORMAL_TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(
            nodes, "**", TextType.BOLD_TEXT), expected)

    def test_multiple_italic_sections(self):
        nodes = [TextNode("This is *italic* and *more italic*",
                          TextType.NORMAL_TEXT)]
        expected = [
            TextNode("This is ", TextType.NORMAL_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" and ", TextType.NORMAL_TEXT),
            TextNode("more italic", TextType.ITALIC_TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(
            nodes, "*", TextType.ITALIC_TEXT), expected)

    def test_no_delimiter(self):
        nodes = [TextNode("Just normal text here", TextType.NORMAL_TEXT)]
        expected = [
            TextNode("Just normal text here", TextType.NORMAL_TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(
            nodes, "`", TextType.CODE_TEXT), expected)

    def test_starts_and_ends_with_delimiter_code(self):
        nodes = [
            TextNode("`code block` and then `another one`", TextType.NORMAL_TEXT)]
        expected = [
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and then ", TextType.NORMAL_TEXT),
            TextNode("another one", TextType.CODE_TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(
            nodes, "`", TextType.CODE_TEXT), expected)

        nodes_alt = [TextNode("`code block`", TextType.NORMAL_TEXT)]
        expected_alt = [
            TextNode("code block", TextType.CODE_TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(
            nodes_alt, "`", TextType.CODE_TEXT), expected_alt)

    def test_mixed_content_with_links_and_bold(self):
        nodes = [
            TextNode("This is ", TextType.NORMAL_TEXT),
            TextNode("a link", TextType.LINK, "http://example.com"),
            TextNode(" and then **bold text** followed by more normal.",
                     TextType.NORMAL_TEXT),
            TextNode("And an image", TextType.IMAGE,
                     "http://example.com/img.png")
        ]
        expected = [
            TextNode("This is ", TextType.NORMAL_TEXT),
            TextNode("a link", TextType.LINK, "http://example.com"),
            TextNode(" and then ", TextType.NORMAL_TEXT),
            TextNode("bold text", TextType.BOLD_TEXT),
            TextNode(" followed by more normal.", TextType.NORMAL_TEXT),
            TextNode("And an image", TextType.IMAGE,
                     "http://example.com/img.png")
        ]
        self.assertEqual(split_nodes_delimiter(
            nodes, "**", TextType.BOLD_TEXT), expected)

    def test_invalid_markdown_uneven_delimiters(self):
        nodes = [TextNode("This is **bold but not closed",
                          TextType.NORMAL_TEXT)]
        with self.assertRaisesRegex(Exception, "invalid Markdown syntax"):
            split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def passing_image_into_link(self):
        node = TextNode(
            "This is text with an ![link](https://i.imgur.com/zjjcJKZ.png) and another ![second link](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )
