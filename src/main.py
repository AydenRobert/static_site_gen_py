from generator import generate_pages_recursively
import os
import shutil
import sys


def setup_dirs(public_dir):
    current_dir = os.getcwd()
    if current_dir.split("/")[-1] != "static_site_gen_py":
        raise Exception("in wrong dir aye")
    shutil.rmtree(public_dir, ignore_errors=True)
    shutil.copytree("static", public_dir, dirs_exist_ok=True)


def main():
    base_dir = ""
    content_dir = base_dir + "content"
    template_file = base_dir + "template.html"
    public_dir = base_dir + "docs"
    setup_dirs(public_dir)
    if len(sys.argv) >= 2:
        base_dir = sys.argv[1]
    if len(sys.argv) >= 3:
        public_dir = sys.argv[2]

    generate_pages_recursively(
        content_dir, template_file, public_dir, base_dir)


if __name__ == "__main__":
    main()
