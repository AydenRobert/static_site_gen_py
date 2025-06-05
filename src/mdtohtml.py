import re


from converter import text_node_to_html_node, text_to_textnode, markdown_to_blocks
from block import BlockType
from htmlnode import LeafNode, PNode, ParentNode
from block import block_to_blocktype


def create_html_list(block, list_type):
    parent_node = None
    if list_type == BlockType.UNORDERED_LIST:
        textnodes = list(map(lambda x: LeafNode(
            "li", x.strip()), block[1:].split("\n-")))
        parent_node = ParentNode("ul", list(
            map(lambda x: x, textnodes)))
    if list_type == BlockType.ORDERED_LIST:
        matches = (re.match(r"^\d+\.\s+(.*?)(?:\s\.\.\..*)?$", line)
                   for line in block.splitlines())
        text_list = [match.group(1) for match in matches if match]
        textnodes = list(map(lambda x: LeafNode("li", x), text_list))
        parent_node = ParentNode("ol", list(
            map(lambda x: x, textnodes)))
    return parent_node


def handle_paragraph_nodes(textnodes):
    out_list = list()
    for node in textnodes:
        htmlnode = text_node_to_html_node(node)
        if htmlnode.tag == "b" or htmlnode.tag == "i" or htmlnode.tag == "code":
            if len(out_list) == 0 or not isinstance(out_list[-1], PNode):
                out_list.append(PNode(""))
            out_list[-1].append(htmlnode)
            out_list[-1].value += "{}"
        elif len(out_list) > 0 and isinstance(out_list[-1], PNode) and isinstance(htmlnode, PNode):
            out_list[-1].value += htmlnode.value
        else:
            out_list.append(htmlnode)
    return out_list


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    htmlnodes = list()
    for block in blocks:
        if block == "":
            continue
        block_type = block_to_blocktype(block)
        match block_type:
            case BlockType.HEADING:
                cur_nodes = list()
                for line in block.splitlines():
                    num = line.count("#")
                    text = line.strip().strip("#").strip()
                    cur_nodes.append(LeafNode(f"h{num}", text))
                htmlnodes.extend(cur_nodes)
            case BlockType.CODE:
                text = "\n".join(
                    map(lambda x: x.strip(), block.strip('`').strip().splitlines()))
                child = LeafNode("code", text)
                htmlnodes.append(ParentNode("pre", [child]))
            case BlockType.QUOTE:
                htmlnodes.append(LeafNode("blockquote", block[1:].strip()))
            case BlockType.UNORDERED_LIST:
                htmlnodes.append(create_html_list(block, block_type))
            case BlockType.ORDERED_LIST:
                htmlnodes.append(create_html_list(block, block_type))
            case BlockType.PARAGRAPH:
                text = block.replace("\n", " ")
                htmlnodes.extend(handle_paragraph_nodes(
                    text_to_textnode(text)))

    return ParentNode("div", htmlnodes)
