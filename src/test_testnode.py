import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        

    def test_different(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINKS, url="https://www.google.com")
        self.assertNotEqual(node, node2)
        
        node3 = TextNode("This is a text node", TextType.LINKS, url="https://www.google.com")
        node4 = TextNode("This is a text node", TextType.IMAGES, url="https://www.google.com")
        self.assertNotEqual(node3, node4)
        
        node5 = TextNode("This is a link", TextType.LINKS, url="https://www.google.com")
        node6 = TextNode("This is a text node", TextType.LINKS, url="https://www.google.com")
        self.assertNotEqual(node5, node6)
        
    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINKS, url="https://www.google.com")
        self.assertEqual("TextNode(This is a text node, links, https://www.google.com)", repr(node))
        
        node1 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual("TextNode(This is a text node, bold)", repr(node1))

if __name__ == "__main__":
    unittest.main()
