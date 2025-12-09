import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="h1", value="some text")
        node2 = HTMLNode(tag="h1", value="some text")
        self.assertEqual(node, node2)
    def test_ne(self):
        node = HTMLNode(tag="h1", value="some other text")
        node2 = HTMLNode(tag="h1", value="some text")        
        self.assertNotEqual(node, node2)
    def test_all(self):
        node = HTMLNode(tag="h1", value="some text", children=['one', 'two', 'three'], props={'a': 'yes', 'b': False,})
        node2 = HTMLNode(tag="h1", value="some text", children=['one', 'two', 'three'], props={'a': 'yes', 'b': False,})
        self.assertEqual(node, node2)
    def test_props(self):
        node = HTMLNode(tag="h1", value="some text", children=['one', 'two', 'three'], props={"href": "https://www.google.com", "target": "_blank",})
        self.assertTrue(node.props_to_html() == ' href="https://www.google.com" target="_blank"')

        
if __name__ == "__main__":
    unittest.main()
        
