from file_utils import copy_directory_recursive
from page_generator import generate_pages_recursive

def main():
    copy_directory_recursive("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()