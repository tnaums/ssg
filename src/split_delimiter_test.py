import unittest

from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitDelimiter(unittest.TestCase):
    def test_split_del(self):
        tnode = TextNode("**This** is some very heavy and important text.", TextType.TEXT)
        snode = split_nodes_delimiter([tnode], "**", TextType.BOLD)
        self.assertNotEqual(snode[0], 'TextNode("This", TextType.BOLD, None)')

if __name__ == "__main__":
    unittest.main()
        
