import re


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)


def remove_markdown_images(text):
    return list(filter(lambda x: x != "",
                re.sub(r"!\[(.*?)\]\((.*?)\)", ".,.,.*.*.,.,.", text)
                       .split(".,.,.")))


def remove_markdown_links(text):
    return list(filter(lambda x: x != "",
                re.sub(r"(?<!\!)\[(.*?)\]\((.*?)\)", ".,.,.*.*.,.,.", text)
                       .split(".,.,.")))
