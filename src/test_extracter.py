import unittest


from extracter import *


class TestExtracter(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_emi_nothing(self):
        matches = extract_markdown_images(
            "This should return an empty list"
        )
        self.assertListEqual([], matches)

    def test_emi_just_square(self):
        matches = extract_markdown_images(
            "This should return an [empty] list"
        )
        self.assertListEqual([], matches)

    def test_eml_mult(self):
        matches = extract_markdown_links(
            "this is link [one](link.to.something) and this is number [two](link.to.something.again)"
        )
        self.assertListEqual(
            [("one", "link.to.something"), ("two", "link.to.something.again")], matches)
