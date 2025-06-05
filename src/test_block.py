import unittest


from block import *


class TestBlock(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_blocktype("# A heading"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype(
            "### Another heading"), BlockType.HEADING)

    def test_heading_malformed(self):
        self.assertEqual(block_to_blocktype(
            "Not # a heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("Plain text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype(
            ""), BlockType.PARAGRAPH)

    def test_code(self):
        self.assertEqual(block_to_blocktype(
            "```python\nprint('hello')\n```"), BlockType.CODE)
        self.assertEqual(block_to_blocktype(
            "```Just the start"), BlockType.CODE)
        self.assertEqual(block_to_blocktype("```"), BlockType.CODE)

    def test_code_malformed(self):
        self.assertEqual(block_to_blocktype("``not code"),
                         BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype(
            "plain text ````"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("``"), BlockType.PARAGRAPH)

    def test_quote(self):
        self.assertEqual(block_to_blocktype(
            "> A quote\n> Continued quote"), BlockType.QUOTE)
        self.assertEqual(block_to_blocktype(
            ">Single line quote"), BlockType.QUOTE)

    def test_quote_malformed(self):
        self.assertEqual(block_to_blocktype(
            "Not > a quote"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype(
            "< Also not a quote"), BlockType.PARAGRAPH)

    def test_ul(self):
        self.assertEqual(block_to_blocktype(
            "- item 1\n- item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_blocktype(
            "- item 1"), BlockType.UNORDERED_LIST)

    def test_ul_malformed(self):
        self.assertEqual(block_to_blocktype(
            "- item 1\nitem 2 (not UL)"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype(
            "* item 1\n* item 2"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype(
            "No list here"), BlockType.PARAGRAPH)

    def test_ol(self):
        self.assertEqual(block_to_blocktype(
            "1. item 1\n2. item 2"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_blocktype(
            "1. item 1"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_blocktype(
            "1. item 1\nWRONG LINE\n3. item 3 makes it OL"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_blocktype(
            "1. first\n2. second\n3. third\n4. fourth\n5. fifth\n6. sixth\n7. seventh\n8. eighth\n9. ninth"), BlockType.ORDERED_LIST)

    def test_ol_malformed(self):
        self.assertEqual(block_to_blocktype("1. item1\n2 item2"),
                         BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype(
            "1. item 1\n3. item 2 (breaks sequence, last line i=2 fails)"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype(
            "a. item 1\nb. item 2"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype(
            "1. item1\n2. item2\n3. item3\n4. item4\n5. item5\n6. item6\n7. item7\n8. item8\n9. item9\n10. item10 (fails due to i=10)"), BlockType.PARAGRAPH)
