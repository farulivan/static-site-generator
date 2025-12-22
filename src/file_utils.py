import os
import shutil

def copy_directory_recursive(src_dir, dest_dir):
    """
    Recursively copies all contents from src_dir to dest_dir.
    First deletes all contents of dest_dir to ensure a clean copy.
    Logs the path of each file copied.
    """
    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Source directory '{src_dir}' does not exist")
    
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    os.makedirs(dest_dir, exist_ok=True)
    
    for root, dirs, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        rel_path = "" if rel_path == "." else rel_path
        dest_root = os.path.join(dest_dir, rel_path)
        if not os.path.exists(dest_root):
            os.makedirs(dest_root)
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_root, file)
            shutil.copy2(src_file, dest_file)
            print(f"Copied {src_file} to {dest_file}")
