from textnode import TextNode, TextType
from extracter import *


def split_text(text_list, text_type, offset):
    if len(text_list) == 0:
        return list()
    out_list = list()
    if text_list[0] != "":
        out_list.append(
            TextNode(text_list[0], TextType.NORMAL_TEXT if offset is False else text_type))
    out_list.extend(split_text(text_list[1:], text_type, not offset))
    return out_list


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    out_list = list()
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            out_list.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"invalid Markdown syntax:\n\t{node}")
        stripped_text = node.text.strip(delimiter)
        if node.text[0] != stripped_text[0]:
            out_list.extend(split_text(
                stripped_text.split(delimiter), text_type, True))
            continue
        text_list = node.text.split(delimiter)
        if len(text_list) == 1:
            out_list.append(node)
            continue
        out_list.extend(split_text(text_list, text_type, False))
    return out_list


def split_nodes_image(old_nodes):
    out_list = list()
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            out_list.append(node)
            continue
        text_list = map(lambda x: TextNode(
            x, TextType.NORMAL_TEXT), remove_markdown_images(node.text))
        image_list = map(lambda x: TextNode(
            x[0], TextType.IMAGE, x[1]), extract_markdown_images(node.text))
        iter_i = iter(image_list)
        out_list.extend(
            map(lambda x: x if x.text != "*.*" else next(iter_i), text_list))
    return out_list


def split_nodes_link(old_nodes):
    out_list = list()
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            out_list.append(node)
            continue
        text_list = map(lambda x: TextNode(
            x, TextType.NORMAL_TEXT), remove_markdown_links(node.text))
        link_list = map(lambda x: TextNode(
            x[0], TextType.LINK, x[1]), extract_markdown_links(node.text))
        iter_i = iter(link_list)
        out_list.extend(
            map(lambda x: x if x.text != "*.*" else next(iter_i), text_list))
    return out_list
