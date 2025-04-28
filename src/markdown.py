import re

from textnode import TextNode, TextType
from htmlnode import ParentNode, text_node_to_html_node
from block import block_to_block_type

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		new = node.text.split(delimiter)
		styled = False
		for split in new:
			if styled:
				new_nodes.append(TextNode(split, text_type))
			else:
				new_nodes.append(TextNode(split, node.text_type))
			styled = not styled
	return new_nodes

def extract_markdown_images(text:str) -> list[tuple]:
	matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def extract_markdown_links(text:str) -> list[tuple]:
	matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
	new_nodes = []

	for node in old_nodes:
		matches = re.finditer(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)

		i = 0
		for match in matches:
			if match.start() != 0:
				temp_node = TextNode(node.text[i:match.start()], node.text_type)
				new_nodes.append(temp_node)
			match_text = extract_markdown_images(match.group())
			image_text_node = TextNode(match_text[0][0], TextType.IMAGE, url=match_text[0][1])
			new_nodes.append(image_text_node)
			i = match.end()
		if i == 0:
			new_nodes.append(node)
		elif i < len(node.text):
			temp_node = TextNode(node.text[i:], node.text_type)
			new_nodes.append(temp_node)
	return new_nodes

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		matches = re.finditer(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)

		i = 0
		for match in matches:
			temp_node = TextNode(node.text[i:match.start()], node.text_type)
			new_nodes.append(temp_node)
			match_text = extract_markdown_links(match.group())
			link_text_node = TextNode(match_text[0][0], TextType.LINK, url=match_text[0][1])
			new_nodes.append(link_text_node)
			i = match.end()
		if i == 0:
			new_nodes.append(node)
		elif i < len(node.text):
			temp_node = TextNode(node.text[i:], node.text_type)
			new_nodes.append(temp_node)
	return new_nodes

def text_to_textnodes(text:str) -> list[TextNode]:
	markdown_node = TextNode(text, "text")
	bold_split = split_nodes_delimiter([markdown_node], "**", "bold")
	italic_split = split_nodes_delimiter(bold_split, "_", "italic")
	code_split = split_nodes_delimiter(italic_split, "`", "code")
	
	images_split = split_nodes_image(code_split)
	link_split = split_nodes_link(images_split)
	return link_split

def markdown_to_blocks(markdown:str) -> list[str]:
	blocks = []
	split = markdown.split("\n\n")
	for block in split:
		temp = block.strip()
		if temp != "":
			blocks.append(temp)
	return blocks

def markdown_to_html_node(markdown:str) -> ParentNode:
	blocks = markdown_to_blocks(markdown)
	children_nodes = []

	for block in blocks:
		temp_text_node = TextNode("", "text")
		block_type = block_to_block_type(block)

		match block_type:
			case "code":
				temp_text_node.text_type = TextType.CODE
				temp_text_node.text = block[3:-3]
				code_node = text_node_to_html_node(temp_text_node)
				children_nodes.append(ParentNode("pre", [code_node]))
			case "heading":
				h_type = 0
				for char in block:
					if char != "#":
						break
					h_type += 1
				temp_text_node.text = block.split(" ", 1)[1]
				heading_node = text_node_to_html_node(temp_text_node)
				heading_node.tag = f"h{h_type}"
				children_nodes.append(heading_node)
			case "unordered_list":
				list_items = block.splitlines()
				list_nodes = []
				for line in list_items:
					text = line.split(" ", 1)[1]
					list_sub_nodes = text_to_textnodes(text)
					list_nodes.append(ParentNode("li", [text_node_to_html_node(x) for x in list_sub_nodes]))
				children_nodes.append(ParentNode("ul", list_nodes))
			case "ordered_list":
				list_items = block.splitlines()
				list_nodes = []
				for line in list_items:
					text = line.split(" ", 1)[1]
					list_sub_nodes = text_to_textnodes(text)
					list_nodes.append(ParentNode("li", [text_node_to_html_node(x) for x in list_sub_nodes]))
				children_nodes.append(ParentNode("ol", list_nodes))
			case "quote":
				quote_lines = block.splitlines()
				stripped_text = '\n'.join([x.lstrip('>') for x in quote_lines])
				sub_quote_nodes = text_to_textnodes(stripped_text.strip())
				children_nodes.append(ParentNode("blockquote", [text_node_to_html_node(x) for x in sub_quote_nodes]))
			case "paragraph":
				paragraph_lines = block.splitlines()
				stripped_text = ' '.join(paragraph_lines)
				paragraph_sub_nodes = text_to_textnodes(stripped_text)
				sub_html_nodes = [text_node_to_html_node(x) for x in paragraph_sub_nodes]
				children_nodes.append(ParentNode("p", sub_html_nodes))

	parent_node = ParentNode(tag="div", children=children_nodes)
	return parent_node

def extract_title(markdown:str) -> str:
	html_node = markdown_to_html_node(markdown)
	for node in html_node.children:
		if node.tag == "h1":
			return node.value
	raise Exception("no title found")
