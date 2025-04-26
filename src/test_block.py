import unittest

import block

class TestBlock(unittest.TestCase):
	def test_block_to_block_type(self):
		test_block1 = "This is **bolded** paragraph"
		block_type = block.block_to_block_type(test_block1)
		self.assertEqual(block_type, "paragraph")

		test_block2 = "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line"
		block_type = block.block_to_block_type(test_block2)
		self.assertEqual(block_type, "paragraph")

		test_block3 = "- This is a list\n- with items"
		block_type = block.block_to_block_type(test_block3)
		self.assertEqual(block_type, "unordered_list")

	def test_block_heading(self):
		test_block1 = "### This is a heading"
		block_type = block.block_to_block_type(test_block1)
		self.assertEqual(block_type, "heading", msg=test_block1)

		test_block2 = "###This is NOT a heading and should be a paragraph"
		block_type = block.block_to_block_type(test_block2)
		self.assertEqual(block_type, "paragraph", msg=test_block2)

		test_block3 = "###### This is another heading"
		block_type = block.block_to_block_type(test_block3)
		self.assertEqual(block_type, "heading", msg=test_block3)

		test_block4 = "####### This is too many hashtags"
		block_type = block.block_to_block_type(test_block4)
		self.assertEqual(block_type, "paragraph", msg=test_block4)

	def test_block_code(self):
		test_block1 = "``` This is a \n code block  ```"
		block_type = block.block_to_block_type(test_block1)
		self.assertEqual(block_type, "code")

		test_block2 = "`` This is NOT a code block  ``"
		block_type = block.block_to_block_type(test_block2)
		self.assertEqual(block_type, "paragraph")

	def test_block_quote(self):
			test_block1 = ">This is a quote block"
			block_type = block.block_to_block_type(test_block1)
			self.assertEqual(block_type, "quote")

			test_block2 = ">This is also a quote \n>block"
			block_type = block.block_to_block_type(test_block2)
			self.assertEqual(block_type, "quote")

			test_block3 = ">This is not a quote \n block"
			block_type = block.block_to_block_type(test_block3)
			self.assertEqual(block_type, "paragraph", msg=test_block3)


	def test_block_unordered_list(self):
			test_block1 = "- This is an unordered list"
			block_type = block.block_to_block_type(test_block1)
			self.assertEqual(block_type, "unordered_list")

			test_block2 = "- This is also an unordered list \n- block"
			block_type = block.block_to_block_type(test_block2)
			self.assertEqual(block_type, "unordered_list")

			test_block3 = "- This is not an unordered_list \n-block"
			block_type = block.block_to_block_type(test_block3)
			self.assertEqual(block_type, "paragraph", msg=test_block3)

	def test_block_ordered_list(self):
				test_block1 = "1. This is an ordered list"
				block_type = block.block_to_block_type(test_block1)
				self.assertEqual(block_type, "ordered_list")

				test_block2 = "1. This is also an ordered list \n2. block"
				block_type = block.block_to_block_type(test_block2)
				self.assertEqual(block_type, "ordered_list")

				test_block3 = "1. This is not an ordered_list \n1. block"
				block_type = block.block_to_block_type(test_block3)
				self.assertEqual(block_type, "paragraph", msg=test_block3)
