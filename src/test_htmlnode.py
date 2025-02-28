import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
	def test_props_to_html(self):
		node_props = {
			"href":"https://www.google.com",
			"target":"_blank"
		}
		node = HTMLNode(props=node_props)
		self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')

	def test_repr(self):
		node_props = {
			"href":"https://www.google.com",
			"target":"_blank"
		}
		child_node = HTMLNode(tag="ChildTag", value="ChildValue")

		node = HTMLNode( \
				tag="TagTest", value="ValueTest", \
				children=child_node, props=node_props)
		print(repr(node))
	
	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_body(self):
		node = LeafNode("body", "Hello, world!")
		self.assertEqual(node.to_html(), "<body>Hello, world!</body>")

	def test_leaf_to_html_no_tag(self):
		node = LeafNode(None, "Hello, world!")
		self.assertEqual(node.to_html(), "Hello, world!")
