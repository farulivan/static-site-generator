from file_utils import copy_directory_recursive

def main():
    copy_directory_recursive("static", "public")

if __name__ == "__main__":
    main()