import unittest

from markdown_blocks import block_to_block_type, BlockType

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
        
if __name__ == "__main__":
    unittest.main()
