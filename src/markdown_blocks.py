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
    Given a quote block, remove the '>' symboles and return text
    """
    final_str = ""
    lines = block.split('\n')
    for line in lines:
        final_str = final_str + line[1:] + "\n"
    return final_str
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        leaves = []
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            list_of_textnodes = text_to_textnodes(block)
            for x in list_of_textnodes:
                new_leaf = text_node_to_html_node(x)
                leaves.append(new_leaf)
            parent_node = ParentNode("p", leaves)
            block_nodes.append(parent_node.to_html())
        if block_type == BlockType.HEADING:
            h_level, text = heading_parser(block)
            list_of_textnodes = text_to_textnodes(text)
            for x in list_of_textnodes:
                new_leaf = text_node_to_html_node(x)
                leaves.append(new_leaf)
            parent_node = ParentNode(h_level, leaves)
            block_nodes.append(parent_node.to_html())
        if block_type == BlockType.CODE:
            text = code_parser(block)
            text_node = TextNode(text, TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            block_nodes.append(html_node.to_html())
        if block_type == BlockType.QUOTE:
            print("found a quote!")
            text = quote_parser(block)
            list_of_textnodes = text_to_textnodes(text)
            for x in list_of_textnodes:
                new_leaf = text_node_to_html_node(x)
                leaves.append(new_leaf)
            parent_node = ParentNode("blockquote", leaves)
            block_nodes.append(parent_node.to_html())
    for block_node in block_nodes:
        print(block_node)
        print()

md = """ 
# Major **heading** here!

For my first try, I am creating a simple paragraph that contains
some simple **bolded sections** and also something that is italic,
like the scientific name of _Escherichia coli_. Hopefully this simple
paragraph will get things started.

## Secondary _italic heading_ here

The second block, also a simple paragraph. I'm including a code block. It is `x = mylist`. I need to figure out how to not parse text that is in a code block. This will allow simple things like variable names with underscores.

###### Lowest level heading **here**

>This represents a line that is a quote.
>All lines must start with
>The gt symbol.

```
print('hello')
print(my_variable)
# comment
print('world')
```
"""
markdown_to_html_node(md)
