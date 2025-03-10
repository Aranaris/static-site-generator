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
