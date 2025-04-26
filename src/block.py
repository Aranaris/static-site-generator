from enum import Enum

import re

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

def block_to_block_type(block:str) -> BlockType:
	match block[0]:
		case "#":
			if re.search(r"^(\#)\1+ ", block) and not re.search(r"^(\#)\1{6}+ ", block):
				return "heading"
		case "`":
			if re.search(r"^(\`)\1{2}", block) and re.search(r"(\`)\1{2}", block):
				return "code"
		case ">":
			split_blocks = block.splitlines()
			for line in split_blocks:
				if line[0] != ">":
					return "paragraph"
			return "quote"
		case "-":
			split_blocks = block.splitlines()
			for line in split_blocks:
				if line[:2] != "- ":
					return "paragraph"
			return "unordered_list"
		case "1":
			split_blocks = block.splitlines()
			line_increment = 1
			for line in split_blocks:
				if line[:3] != f"{line_increment}. ":
					return "paragraph"
				line_increment += 1
			return "ordered_list"
	return "paragraph"
