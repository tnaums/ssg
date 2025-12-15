import sys
import os
import shutil
from markdown_blocks import markdown_to_blocks, markdown_to_html_node

def empty_public():
    target = 'docs'
    try:
        shutil.rmtree(target)
    except FileNotFoundError:
        pass
    os.mkdir(target)

def copy_to_public(source_dir, target_dir):
    contents = os.listdir(source_dir)
    for content in contents:
        path = os.path.join(source_dir, content)
        if os.path.isfile(path):
            shutil.copy(path, target_dir)
        elif os.path.isdir(path):
            new_dir = os.path.join("docs", content)
            os.mkdir(new_dir)
            copy_to_public(path, new_dir)


def extract_title(markdown):
    h1_header = ""
    lines = markdown.split("/n")
    for line in lines:
        if line.startswith("#"):
            h1_header = line[1:]
            h1_header = h1_header.strip()
    if h1_header == "":
        raise Exception("No h1 header found in markdown file.")
    else:
        return h1_header

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as t:
        template = t.read()
    node = markdown_to_html_node(markdown)
    html = node.to_html()
    the_title = extract_title(markdown)
    update_string = template.replace("{{ Title }}", the_title)
    final_string = update_string.replace("{{ Content }}", html)
    new_href = f'href="{basepath}'
    new_src = f'src="{basepath}'
    final_string = final_string.replace('href="/', new_href)
    final_string = final_string.replace('src="/', new_src)
    with open(dest_path, 'w') as out:
        out.write(final_string)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
     contents = os.listdir(dir_path_content)
     for content in contents:
        path = os.path.join(dir_path_content, content)
        target = os.path.join(dest_dir_path, content)
        if os.path.isfile(path) and path.endswith('md'):
            target = target.replace('md', 'html')
            generate_page(path, template_path, target, basepath)
        elif os.path.isdir(path):
            os.mkdir(target)
            generate_pages_recursive(path, template_path, target, basepath)            

    
def main():
    try:
        basepath = sys.argv[1]
    except IndexError:
        basepath = "/"
    empty_public()
    copy_to_public('static', 'docs')
    generate_pages_recursive('content', 'template.html', 'docs', basepath)

if __name__ == "__main__":
    main()
    
