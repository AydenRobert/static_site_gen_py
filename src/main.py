import os
import shutil


def main():
    current_dir = os.getcwd()
    if current_dir.split("/")[-1] != "static_site_gen_py":
        raise Exception("in wrong dir aye")
    os.rmdir("public")
    shutil.copytree("static", "public", dirs_exist_ok=True)

if __name__ == "__main__":
    main()
