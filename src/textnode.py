from enum import Enum

class TextType(Enum):
	NORMAL = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINKS = "links"
	IMAGES = "images"


class TextNode():
	def __init__(self, text:str, text_type:str, **kwargs) -> None:
		self.text = text
		self.text_type = TextType(text_type)
		self.url = kwargs.get("url", None)

	def __eq__(self, value: object) -> bool:
		if self.text == value.text and self.text_type == value.text_type and self.url == value.url:
			return True
		return False
	
	def __repr__(self) -> str:
		return f"TextNode({self.text}, {self.text_type.value}{", " + self.url if self.url is not None else ""})"
