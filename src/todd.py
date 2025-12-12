from textnode import TextNode
from textnode import TextType
from inline_markdown import split_nodes_delimiter

def main():
    md = """
This is some **text** that should be converted from _markdown_ to _html_. It should also include some code, like ``print(myvarname)``. After three calls to ``splitnodesdelimiter``, it should be properly **formatted.**
"""
    original = TextNode(md, TextType.TEXT)
    nodes = [original]
    arguments = [("**", TextType.BOLD), ("_", TextType.ITALIC), ("``", TextType.CODE)]
    for argument in arguments:
        delimiter, ttype = argument
        nodes = split_nodes_delimiter(nodes, delimiter, ttype)
    for node in nodes:
        print(node)



main()
