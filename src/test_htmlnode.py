import unittest

from htmlnode import HTMLNode

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
	
