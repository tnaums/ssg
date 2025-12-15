import re
from enum import Enum
from inline_markdown import text_to_textnodes
from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
    
def markdown_to_blocks(text):
    final_list = []
    candidates_list = text.split("\n\n")
    for candidate in candidates_list:
        if candidate == "":
            continue
        else:
            final_list.append(candidate.strip())
    return final_list

def block_to_block_type(text):
    heading = re.compile(r'#{1,6} .*')
    code = re.compile(r'^```.*```$', flags=re.DOTALL)
    if code.search(text):
        return BlockType.CODE
    if heading.search(text):
        return BlockType.HEADING
    is_quote = True
    is_unordered = True
    is_ordered = True
    count_ordered = 1
    line_list = text.split("\n")
    for line in line_list:
        if line == "":
            continue
        if not line.startswith('>'):
            is_quote = False
        if not line.startswith('-'):
            is_unordered = False
        if not line.startswith(str(count_ordered) + '.' + ' '):
            is_ordered = False
        count_ordered += 1
    if is_quote:
        return BlockType.QUOTE
    if is_unordered:
        return BlockType.UNORDERED_LIST
    if is_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def paragraph_parser(block):
    return block.replace("\n", " ")

def heading_parser(block):
    """
    Given a heading block, return both the 'h' number and the heading text
    with the '#' removed
    """
    determine_h_number = re.compile(r'^(#{1,6}) (.*)')
    for match in determine_h_number.findall(block):
        left, right = match
        h_level = "h" + str(len(left))
        return h_level, right

def code_parser(block):
    """
    Given a code block, removes the delimiters and returns the text
    """
    extract_text = re.compile(r'^```(.*)```$', flags=re.DOTALL)
    match_list = extract_text.findall(block)
    return match_list[0]

def quote_parser(block):
    """
    Given a quote block, remove the '>' symbles and return text
    """
    final_str = ""
    lines = block.split('\n')
    print(f"block quote parser: lines are {lines}")
    for line in lines:
        final_str = final_str + line[2:]# + "\n"
    print(f"final string: {final_str}")
    return final_str

def unordered_list_parser(block):
    """
    Given unordered list block: 
    replaces '-' with <li>
    replaces '\n' with </li>
    and returns the text string.
    """
    final_str = block.replace("- ", "<li>")
    final_str = final_str.replace("\n", "</li>")
    return final_str

def ordered_list_parser(block):
    """
    Given ordered list block:
    adds <li> and </li> to ends of each element.
    """
    x = re.compile(r'\d+\.\ (.*)')
    final_str = ""
    matches = x.findall(block)
    for match in matches:
        to_add = f"<li>{match}</li>"
        final_str = final_str + to_add
    return final_str
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        leaves = []
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            text = paragraph_parser(block)
            list_of_textnodes = text_to_textnodes(text)
            for x in list_of_textnodes:
                new_leaf = text_node_to_html_node(x)
                leaves.append(new_leaf)
            parent_node = ParentNode("p", leaves)
            block_nodes.append(parent_node)
        if block_type == BlockType.HEADING:
            h_level, text = heading_parser(block)
            list_of_textnodes = text_to_textnodes(text)
            for x in list_of_textnodes:
                new_leaf = text_node_to_html_node(x)
                leaves.append(new_leaf)
            parent_node = ParentNode(h_level, leaves)
            block_nodes.append(parent_node)
        if block_type == BlockType.CODE:
            text = code_parser(block)
            text_node = TextNode(text, TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            block_nodes.append(html_node)
        if block_type == BlockType.QUOTE:
            text = quote_parser(block)
            list_of_textnodes = text_to_textnodes(text)
            for x in list_of_textnodes:
                new_leaf = text_node_to_html_node(x)
                leaves.append(new_leaf)
            parent_node = ParentNode("blockquote", leaves)
            block_nodes.append(parent_node)
        if block_type == BlockType.UNORDERED_LIST:
            text = unordered_list_parser(block)
            list_of_textnodes = text_to_textnodes(text)
            for x in list_of_textnodes:
                new_leaf = text_node_to_html_node(x)
                leaves.append(new_leaf)
            parent_node = ParentNode("ul", leaves)
            block_nodes.append(parent_node)
        if block_type == BlockType.ORDERED_LIST:
            text = ordered_list_parser(block)
            list_of_textnodes = text_to_textnodes(text)
            for x in list_of_textnodes:
                new_leaf = text_node_to_html_node(x)
                leaves.append(new_leaf)
            parent_node = ParentNode("ol", leaves)
            block_nodes.append(parent_node)
    return ParentNode("div", block_nodes)


def extract_title(markdown):
    h1_header = ""
    for line in markdown:
        if line.startswith("# "):
            h1_header = line[2:]
            h1_header = h1_header.strip()
    if h1_header == "":
        raise Exception("No h1 header found in markdown file.")
    else:
        return h1_header

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as t:
        template = t.read()
    html_string = markdown_to_html_node(markdown).to_html()
    the_title = extract_title(markdown)
    update_string = template.replace("{{ Title }}", the_title)
    final_string = update_string.replace("{{ Content }}", html_string)
    with open(dest_path, 'w') as out:
        out.write(final_string)
        

    
# md = """ 
# # Major **heading** here!

# For my first try, I am creating a simple paragraph that contains
# some simple **bolded sections** and also something that is italic,
# like the scientific name of _Escherichia coli_. Hopefully this simple
# paragraph will get things started.

# ## Secondary _italic heading_ here

# The second block, also a simple paragraph. I'm including a code block. It is `x = mylist`. I need to figure out how to not parse text that is in a code block. This will allow simple things like variable names with underscores.

# ###### Lowest level heading **here**

# >This represents a line that is a quote.
# >All lines must start with
# >The gt symbol.

# - unordered list
# - with some points
# - for people to ponder

# 1. begining ordered list
# 2. with a couple of
# 3. important points.

# ```
# print('hello')
# print(my_variable)
# # comment
# print('world')
# ```
# """
# document = markdown_to_html_node(md)
# print(document.to_html())
