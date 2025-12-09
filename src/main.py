from textnode import TextNode
from textnode import TextType

def main():
    tnode1 = TextNode("Some illin text", TextType.BOLD, "https://www.boot.dev")
    print(tnode1)
    tnode2 = TextNode("Other text here", TextType.BOLD, "https://www.boot.dev")
    print(tnode1 == tnode2)

main()
