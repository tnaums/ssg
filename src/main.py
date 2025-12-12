from textnode import TextNode
from textnode import TextType
from split_delimiter import split_nodes_delimiter

def main():
    # tnode1 = TextNode("Some illin text", TextType.BOLD, "https://www.boot.dev")
    # print(tnode1)
    # tnode2 = TextNode("Other text here", TextType.BOLD, "https://www.boot.dev")
    # print(tnode1 == tnode2)
    tnode3 = TextNode("This is some **very heavy** and important text.", TextType.TEXT)
    split_nodes_delimiter([tnode3], "**", TextType.BOLD)
    tnode4 = TextNode("This is **also** some **very heavy** and important text.", TextType.TEXT)
#    split_nodes_delimiter([tnode4], "**", TextType.BOLD)
    tnode5 = TextNode("**This** is some very heavy and important text.", TextType.TEXT)
    print(split_nodes_delimiter([tnode5], "**", TextType.BOLD))

main()
