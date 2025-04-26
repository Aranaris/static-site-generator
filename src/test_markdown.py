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
	
	def test_extract_markdown_images(self):
		text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
		extracted_text = markdown.extract_markdown_images(text)
		expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

		self.assertEqual(extracted_text, expected)

	def test_extract_markdown_links(self):
		text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
		extracted_text = markdown.extract_markdown_links(text)
		
		expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

		self.assertEqual(extracted_text, expected)

	def test_split_nodes_link(self):
		node = TextNode(
				"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
				TextType.TEXT,
		)
		new_nodes = markdown.split_nodes_link([node])

		expected = [
				TextNode("This is text with a link ", TextType.TEXT),
				TextNode("to boot dev", TextType.LINK, url="https://www.boot.dev"),
				TextNode(" and ", TextType.TEXT),
				TextNode(
						"to youtube", TextType.LINK, url="https://www.youtube.com/@bootdotdev"
				),
		]

		self.assertEqual(new_nodes, expected)

	def test_split_nodes_image(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.TEXT,
		)

		new_nodes = markdown.split_nodes_image([node])

		expected = [
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.TEXT),
				TextNode(
					"second image", TextType.IMAGE, url="https://i.imgur.com/3elNhQu.png"
				),
			]
		
		self.assertEqual(
			new_nodes,
			expected
		)
	
	def test_text_to_textnodes(self):
		text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

		new_nodes = markdown.text_to_textnodes(text)

		expected = [
				TextNode("This is ", TextType.TEXT),
				TextNode("text", TextType.BOLD),
				TextNode(" with an ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
				TextNode(" word and a ", TextType.TEXT),
				TextNode("code block", TextType.CODE),
				TextNode(" and an ", TextType.TEXT),
				TextNode("obi wan image", TextType.IMAGE, url="https://i.imgur.com/fJRm4Vk.jpeg"),
				TextNode(" and a ", TextType.TEXT),
				TextNode("link", TextType.LINK, url="https://boot.dev"),
		]

		self.assertEqual(
			new_nodes,
			expected
		)

	def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
		"""
		blocks = markdown.markdown_to_blocks(md)
		self.assertEqual(
				blocks,
				[
						"This is **bolded** paragraph",
						"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
						"- This is a list\n- with items",
				],
		)
		
	def test_paragraphs(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

		node = markdown.markdown_to_html_node(md)
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

		node = markdown.markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
		)

	def test_headingblock(self):
		md = "### This is a heading"

		node = markdown.markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><h3>This is a heading</h3></div>"
		)

	def test_unorderedlistblock(self):
		md = """
- This is a list
- with items
		"""

		node = markdown.markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ul><li>This is a list</li><li>with items</li></ul></div>"
		)

	def test_orderedlistblock(self):
		md = """
1. This is an ordered list
2. with items
		"""

		node = markdown.markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ol><li>This is an ordered list</li><li>with items</li></ol></div>"
		)

	def test_quoteblock(self):
		md = """
>This is a quote block
>with multiple lines
		"""

		node = markdown.markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><quoteblock>This is a quote block\nwith multiple lines</quoteblock></div>"
		)
