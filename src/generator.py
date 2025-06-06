from extracter import extract_title
from mdtohtml import markdown_to_html_node
import os


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path).read()
    template = open(template_path).read()
    title = extract_title(markdown)
    htmlnode = markdown_to_html_node(markdown)
    template = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", htmlnode.to_html())
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "a") as dest:
        dest.write(template)


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    mds = list()
    for dirpath, _, filenames in os.walk(dir_path_content):
        paths = list(map(lambda y: f"{dirpath}/{y}",
                     filter(lambda x: x.endswith(".md"), filenames)))
        if len(paths) == 0:
            continue
        mds.extend(paths)
    for md in mds:
        mdpath = md
        htmlpath = md.replace(f"{dir_path_content}/",
                              f"{dest_dir_path}/").replace(".md", ".html")
        generate_page(mdpath, template_path, htmlpath)
