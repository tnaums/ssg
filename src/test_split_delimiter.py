import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from inline_markdown import split_nodes_image, split_nodes_link, text_to_textnodes 
from textnode import TextNode, TextType
from markdown_blocks import markdown_to_blocks


class TestSplitDelimiter(unittest.TestCase):
    def test_split_del(self):
        tnode = TextNode("**This** is some very heavy and important text.", TextType.TEXT)
        snode = split_nodes_delimiter([tnode], "**", TextType.BOLD)
        self.assertEqual(snode[0], TextNode("This", TextType.BOLD, None))
    def test_split_del_2(self):
        tnode = TextNode("This is some **very heavy** and important text.", TextType.TEXT)
        snode = split_nodes_delimiter([tnode], "**", TextType.BOLD)
        self.assertEqual(snode[1], TextNode("very heavy", TextType.BOLD, None))
    def test_split_end(self):
        tnode = TextNode("This is some **very heavy** and **important text.**", TextType.TEXT)
        snode = split_nodes_delimiter([tnode], "**", TextType.BOLD)
        self.assertEqual(len(snode), 4)
    def test_split_code(self):
        tnode = TextNode("This is some ``for i in range(10):``", TextType.TEXT)
        snode = split_nodes_delimiter([tnode], "``", TextType.CODE)
        print(snode)
        self.assertEqual(snode[1], TextNode("for i in range(10):", TextType.CODE, None))
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "![JRR Tolkien sitting](/images/tolkien.png)"
            )
        self.assertListEqual([("JRR Tolkien sitting", "/images/tolkien.png")], matches)
    def test_extract_markdown_images_two(self):
        matches = extract_markdown_links(
            text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
            ],
        )        
if __name__ == "__main__":
    unittest.main()
        
