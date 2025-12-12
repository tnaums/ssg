import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_with_props_ne(self):
        node = LeafNode("a", "Click me!", {"href": "htps://google.com"})
        self.assertNotEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_with_props_eq(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    def test_simple_eq(self):
        node = LeafNode("p", "This is bold text.")
        self.assertEqual(node.to_html(), '<p>This is bold text.</p>')
    def test_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(repr(node), "LeafNode(a, Click me!, {'href': 'https://www.google.com'})")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_nested_parents(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        outer_parent_node = ParentNode("form", [parent_node])
        self.assertEqual(
            outer_parent_node.to_html(),
            "<form><div><span><b>grandchild</b></span></div></form>"
        )
    def test_repr(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            repr(parent_node),
            "ParentNode(div, [ParentNode(span, [LeafNode(b, grandchild, None)], None)], None)"
            )

if __name__ == "__main__":
    unittest.main()
        
