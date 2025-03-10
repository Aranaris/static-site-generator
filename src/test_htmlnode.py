import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode

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
		children_nodes = [HTMLNode(tag="ChildTag", value="ChildValue")]

		node = HTMLNode( \
				tag="TagTest", value="ValueTest", \
				children=children_nodes, props=node_props)
		self.assertEqual(repr(node), \
			'HTMLNode(Tag: TagTest, Value: ValueTest, Children: [HTMLNode(Tag: ChildTag, Value: ChildValue, Children: [], Props: None)], Props: href="https://www.google.com" target="_blank")')
	
	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_body(self):
		node = LeafNode("body", "Hello, world!")
		self.assertEqual(node.to_html(), "<body>Hello, world!</body>")

	def test_leaf_to_html_no_tag(self):
		node = LeafNode(None, "Hello, world!")
		self.assertEqual(node.to_html(), "Hello, world!")

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

	def test_text_to_html_normal_text(self):
		text_node = TextNode("test string", "text")
		new_node = text_node_to_html_node(text_node)
		html_node = HTMLNode(tag=None, value="test string")
		self.assertEqual(new_node, html_node)


	def test_text_to_html_link_text(self):
		text_node = TextNode("test string", "link", url="https://www.google.com")
		new_node = text_node_to_html_node(text_node)
		props = {
				"href":"https://www.google.com"
			}
		html_node = HTMLNode(tag="a", value="test string", props=props)
		self.assertEqual(new_node, html_node)

	def test_text_to_html_image_node(self):
		text_node = TextNode("test string", "image", url="https://www.google.com")
		new_node = text_node_to_html_node(text_node)
		props = {
				"src":"https://www.google.com",
				"alt":"test string"
			}
		html_node = HTMLNode(tag="img", value="", props=props)
		self.assertEqual(new_node, html_node)
