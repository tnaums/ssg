import unittest

from markdown_blocks import block_to_block_type, BlockType, markdown_to_html_node

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        text = "###### This is a headline"
        heading = block_to_block_type(text)
        self.assertEqual(heading, BlockType.HEADING)
    def test_code(self):
        text = "```print(some_variable)```"
        code = block_to_block_type(text)
        self.assertEqual(code, BlockType.CODE)
    def test_unordered(self):
        text = """
- first line
- second line
- third line
"""
        unordered = block_to_block_type(text)
        self.assertEqual(unordered, BlockType.UNORDERED_LIST)
    def test_ordered(self):
        text = """
1. first item
2. second item
3. third item
"""
        ordered = block_to_block_type(text)
        self.assertEqual(ordered, BlockType.ORDERED_LIST)
class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

        def test_codeblock(self):
            md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )
    
if __name__ == "__main__":
    unittest.main()
