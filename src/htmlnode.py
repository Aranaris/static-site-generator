import textwrap

class HTMLNode():
	def __init__(self, **kwargs) -> None:
		self.tag = kwargs.get("tag", None)
		self.value = kwargs.get("value", None)
		self.children = kwargs.get("children", None)
		self.props = kwargs.get("props", None)

	def to_html(self):
		raise NotImplementedError

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

		node_string = f"HTMLNode( \n\
		Tag: {self.tag}, \n\
		Value: {self.value}, \n\
		Children: {str(self.children) if self.children is not None else self.children}, \n\
		Props: {self.props_to_html()}\n\
		)"

		return textwrap.dedent(node_string)
