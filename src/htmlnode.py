import textwrap
from textnode import TextNode, TextType

class HTMLNode():
	def __init__(self, **kwargs) -> None:
		self.tag = kwargs.get("tag", None)
		self.value = kwargs.get("value", None)
		self.children = kwargs.get("children", None)
		self.props = kwargs.get("props", None)

	def __eq__(self, node: object) -> bool:
		if self.tag == node.tag and \
		self.value == node.value and \
		self.children == node.children and \
		self.props == node.props:
			return True
		return False

	def to_html(self):
		raise NotImplementedError()

	def props_to_html(self) -> str:
		if self.props is None:
			return
		
		html_string = ""
		for x in self.props:
			if html_string != "":
				html_string += " "
			html_string += f'{x}="{self.props[x]}"'
		return html_string

	def __repr__(self) -> str:

		children_string = ""
		if self.children is None:
			children_string = "[]"
		else:
			children_string = ", ".join(map(str, self.children))
			children_string = "[" + children_string + "]"
		node_string = f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Children: {children_string}, Props: {self.props_to_html()})"

		return textwrap.dedent(node_string)
	
class LeafNode(HTMLNode):
	def __init__(self, tag:str, value:str, **kwargs) -> None:
		if kwargs.get("children", None) is not None:
			print("Leaf Node should not have children.")
			return
		super().__init__(tag=tag, value=value, **kwargs)

	def to_html(self):
		if self.value is None:
			raise ValueError("Value cannot be None.")
		
		if self.tag is None:
			return self.value
		
		return f"<{self.tag}>{self.value}</{self.tag}>"
	
class ParentNode(HTMLNode):
	def __init__(self, tag, children, **kwargs) -> None:
		if kwargs.get("value", None) is not None:
			print("Parent Node should not have a value")
		super().__init__(tag=tag, children=children, **kwargs)

	def to_html(self):
		if self.tag is None:
			raise ValueError("Tag cannot be None.")
		if self.children is None:
			raise ValueError("Parent Node must have children.")
		child_string = ""
		for node in self.children:
			child_string += node.to_html()
		return f"<{self.tag}>{child_string}</{self.tag}>"


def text_node_to_html_node(text_node:TextNode) -> HTMLNode:
	match text_node.text_type:
		case TextType.TEXT:
			return LeafNode(tag=None, value=text_node.text)
		case TextType.BOLD:
			return LeafNode(tag="b", value=text_node.text)
		case TextType.ITALIC:
			return LeafNode(tag="i", value=text_node.text)
		case TextType.CODE:
			return LeafNode(tag="code", value=text_node.text)
		case TextType.LINK:
			props = {
				"href":text_node.url
			}
			return LeafNode(tag="a", value=text_node.text, props=props)
		case TextType.IMAGE:
			props = {
				"src":text_node.url,
				"alt":text_node.text
			}
			return LeafNode(tag="img", value="", props=props)
		case _ :
			raise ValueError("Unsupported text type")
