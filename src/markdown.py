from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes:list, delimiter:str, text_type:TextType) -> list:
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
