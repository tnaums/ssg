import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return_list = []
    alt_text = re.compile(r'!\[(.*?)\]')
    image_url = re.compile(r'\((.*?)\)')
    left_matches = alt_text.findall(text)
    right_matches = image_url.findall(text)
    for atext, url in zip(left_matches, right_matches):
        return_list.append((atext, url))
    return return_list

def extract_markdown_links(text):
    return_list = []
    anchor_text = re.compile(r'\[(.*?)\]')
    link_url = re.compile(r'\((.*?)\)')
    left_matches = anchor_text.findall(text)
    right_matches = link_url.findall(text)
    for atext, url in zip(left_matches, right_matches):
        return_list.append((atext, url))
    return return_list


def split_nodes_image(old_nodes):
    new_nodes = []
    image_delimiter = re.compile(r'(!\[.*?\]\(.*?\))')
    for old_node in old_nodes:
        sections = image_delimiter.split(old_node.text)
        if len(sections) == 1:
            new_nodes.append(old_node)
            continue
        print(f"sections => {sections}")
        if len(sections) % 2 == 0:
            raise ValueError("invalid image markdown, formatted section not closed")
        for section in sections:
            if section.startswith('!'):
                list_o_tuples = extract_markdown_images(section)
                for tpl in list_o_tuples:
                    atext, url = tpl
                    print(type(atext), type(url))
                    print(f"atext: {atext}, url: {url}")
                    new_nodes.append(TextNode(atext, TextType.IMAGE, url))
            elif len(section) == 0:
                continue
            else:
                new_nodes.append(TextNode(section, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    image_delimiter = re.compile(r'(\[.*?\]\(.*?\))')
    for old_node in old_nodes:
        sections = image_delimiter.split(old_node.text)
        if len(sections) == 1:
            new_nodes.append(old_node)
            continue
        if len(sections) % 2 == 0:
            raise ValueError("invalid image markdown, formatted section not closed")
        for section in sections:
            if section.startswith('['):
                list_o_tuples = extract_markdown_links(section)
#                print(list_o_tuples)
                for tpl in list_o_tuples:
                    atext, url = tpl
                    new_nodes.append(TextNode(atext, TextType.LINK, url))
            elif len(section) == 0:
                continue
            else:
                new_nodes.append(TextNode(section, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    original_node = TextNode(text, TextType.TEXT)
    nodes = [original_node]
    # First, run through the three split_nodes_delimiter 'modes'
    arguments = [("**", TextType.BOLD), ("_", TextType.ITALIC), ("`", TextType.CODE)]
    for argument in arguments:
        delimiter, ttype = argument
        nodes = split_nodes_delimiter(nodes, delimiter, ttype)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
        

    
