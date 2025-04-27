
import os, shutil

def main():
	with open("run.log", "w") as log_file:
		copy_to_dir("static","public",log_file)

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
	
if __name__ == "__main__":
	main()
