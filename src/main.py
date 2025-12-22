from file_utils import copy_directory_recursive
from page_generator import generate_page

def main():
    copy_directory_recursive("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()