import os
from converters import markdown_to_html_node
from parsers import extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as f:
        markdown = f.read()
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    
    full_html = template.replace('{{ Title }}', title).replace('{{ Content }}', html_content)
    full_html = full_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w') as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                md_path = os.path.join(root, file)
                rel_path = os.path.relpath(md_path, dir_path_content)
                html_path = rel_path.replace('.md', '.html')
                dest_path = os.path.join(dest_dir_path, html_path)
                generate_page(md_path, template_path, dest_path, basepath)
