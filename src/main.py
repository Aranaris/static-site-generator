from markdown import extract_title, markdown_to_html_node


import os, shutil, re

def main():
	with open("run.log", "w") as log_file:
		copy_to_dir("static","public",log_file)

	generate_page("content/index.md", "template.html", "public/index.html")

def copy_to_dir(src_dir:str, dest_dir:str, log_file:object) -> None:
	if not os.path.exists(dest_dir):
		raise FileNotFoundError(f"directory {dest_dir} does not exist")
	
	for filename in os.listdir(dest_dir):
		pathname = os.path.join(dest_dir, filename)
		if os.path.isfile(pathname):
			log_file.write(f"Deleting file {pathname}...\n")
			os.unlink(pathname)
		elif os.path.isdir(pathname):
			shutil.rmtree(pathname)
			log_file.write(f"Deleting directory {pathname}...\n")
		else:
			raise RuntimeError(f"unable to remove file {pathname}")
	
	src_files = os.listdir(src_dir)
	for filename in src_files:
		pathname = os.path.join(src_dir, filename)
		if os.path.isfile(pathname):
			log_file.write(f"Copying file {pathname} to {dest_dir}...\n")
			shutil.copy(pathname, dest_dir)
			
		elif os.path.isdir(pathname):
			dest_pathname = os.path.join(dest_dir, filename)
			log_file.write(f"Creating directory {dest_pathname}...\n")
			os.mkdir(dest_pathname)
			copy_to_dir(pathname, dest_pathname, log_file)
		else:
			raise RuntimeError(f"unable to copy file {pathname}")
	
def generate_page(from_path:str, template_path:str, dest_path:str) -> None:
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	with open(from_path) as md_file:
		md = md_file.read()
	
	with open(template_path) as template_file:
		template = template_file.read()
	
	title = extract_title(md)
	html_node = markdown_to_html_node(md)
	html = html_node.to_html()

	updated_title = re.sub(r"\{\{ Title \}\}", title, template)
	output = re.sub(r"\{\{ Content \}\}", html, updated_title)

	with open(dest_path, "w") as dest_file:
		dest_file.write(output)

if __name__ == "__main__":
	main()
