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


def extract_title(markdown):
    for line in markdown.splitlines():
        if line[0:2] == "# ":
            return line[1:].strip()
    raise Exception("No H1 Header")
