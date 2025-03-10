import unittest

from textnode import TextNode, TextType
import markdown

class TestMarkdown(unittest.TestCase):
	def test_split_nodes_delimiter(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		new_nodes = markdown.split_nodes_delimiter([node], "`", TextType.CODE)

		expected_nodes = [
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("code block", TextType.CODE),
				TextNode(" word", TextType.TEXT),
		]
		self.assertEqual(new_nodes, expected_nodes)

	def test_multi_split_nodes_delimiter(self):
		node = TextNode("This is another text with a **bold** word", TextType.TEXT)
		node2 = TextNode("This is **text** with many bolded **words**", TextType.TEXT)
		new_nodes = markdown.split_nodes_delimiter([node, node2], "**", TextType.BOLD)

		expected_nodes = [
				TextNode("This is another text with a ", TextType.TEXT),
				TextNode("bold", TextType.BOLD),
				TextNode(" word", TextType.TEXT),
				TextNode("This is ", TextType.TEXT),
				TextNode("text", TextType.BOLD),
				TextNode(" with many bolded ", TextType.TEXT),
				TextNode("words", TextType.BOLD),
				TextNode("", TextType.TEXT),
		]
		self.assertEqual(new_nodes, expected_nodes)
