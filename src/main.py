from generator import generate_pages_recursively
import os
import shutil


def setup_dirs():
    current_dir = os.getcwd()
    if current_dir.split("/")[-1] != "static_site_gen_py":
        raise Exception("in wrong dir aye")
    shutil.rmtree("public")
    shutil.copytree("static", "public", dirs_exist_ok=True)


def main():
    setup_dirs()
    generate_pages_recursively("content", "template.html", "public")

if __name__ == "__main__":
    main()
