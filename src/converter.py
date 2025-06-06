from textnode import TextNode, TextType
from htmlnode import LeafNode, PNode, NoneNode
from splitnodes import *


def text_node_to_html_node(text_node, node_type=0):
    match text_node.text_type:
        case TextType.NORMAL_TEXT:
            return PNode(text_node.text) if node_type == 0 else NoneNode(text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url,
                                        "alt_text": text_node.text})


def text_to_textnode(text):
    node_list = split_nodes_image([TextNode(text, TextType.NORMAL_TEXT)])
    node_list = split_nodes_link(node_list)
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD_TEXT)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC_TEXT)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE_TEXT)
    return node_list


def markdown_to_blocks(markdown):
    markdown_list = map(lambda x: x.strip(), markdown.split("\n\n"))
    return list(filter(lambda x: x is not False, markdown_list))
