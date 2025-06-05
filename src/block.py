from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_blocktype(block):
    if len(block) == 0:
        return BlockType.PARAGRAPH
    if block.strip()[0] == "#":
        return BlockType.HEADING
    if block[0:3] == "```" and block[-2:-1]:
        return BlockType.CODE
    if block[0] == ">":
        return BlockType.QUOTE
    if block[0] == "-":
        is_ul = True
        for line in block.split("\n"):
            is_ul = False if line[0] != "-" else True
        return BlockType.UNORDERED_LIST if is_ul is True else BlockType.PARAGRAPH
    if block[0].isnumeric() and block[1] == ".":
        is_ol = True
        i = 0
        for line in block.split("\n"):
            i += 1
            is_ol = True if line[0] == f"{i}" and line[1] == "." else False
        return BlockType.ORDERED_LIST if is_ol is True else BlockType.PARAGRAPH
    return BlockType.PARAGRAPH
