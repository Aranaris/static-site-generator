import re

from textnode import TextNode, TextType

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
	matches = re.findall(r"!\[([^\[\]]*)\]\((\w+:?\/\/[^\s]*)\)", text)
	return matches

def extract_markdown_links(text:str) -> list[tuple]:
	matches = re.findall(r"[^!]\[([^\[\]]*)\]\((\w+:?\/\/[^\s]*)\)", text)
	return matches

def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		matches = re.finditer(r"!\[([^\[\]]*)\]\((\w+:?\/\/[^\s]*)\)", node.text)
		i = 0
		for match in matches:
			temp_node = TextNode(node.text[i:match.start()], node.text_type)
			new_nodes.append(temp_node)
			match_text = extract_markdown_images(match.group())
			image_text_node = TextNode(match_text[0][0], TextType.IMAGE, url=match_text[0][1])
			new_nodes.append(image_text_node)
			i = match.end()
	return new_nodes

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		matches = re.finditer(r"[^!]\[([^\[\]]*)\]\((\w+:?\/\/[^\s]*)\)", node.text)
		i = 0
		for match in matches:
			temp_node = TextNode(node.text[i:match.start() + 1], node.text_type)
			new_nodes.append(temp_node)
			match_text = extract_markdown_links(match.group())
			link_text_node = TextNode(match_text[0][0], TextType.LINK, url=match_text[0][1])
			new_nodes.append(link_text_node)
			i = match.end()
	return new_nodes
