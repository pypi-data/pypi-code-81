import hashlib

def has_hash_changed(current_data, filename):
	current_hash = generate_hash(current_data)
	previous_hash = get_previous_hash(filename)
	return not previous_hash == current_hash

def write_new_hash(current_data, filename):
	current_hash = generate_hash(current_data)
	base_file_name = filename.split(".")[0]
	hash_file_path = f".hashes/{base_file_name}.txt"
	with open(hash_file_path, "w+") as fw:
		fw.write(current_hash)

def generate_hash(data):
	return hashlib.sha256(data.encode("utf8")).hexdigest()

def get_previous_hash(filename):
	base_file_name = filename.split(".")[0]
	hash_file_path = f".hashes/{base_file_name}.txt"
	try:
		with open(hash_file_path, "r") as fr:
			return fr.read()
	except FileNotFoundError:
		return None