def replacement_map(alter: str, replacements: dict):
	for key in replacements.keys():
		alter = alter.replace(key, replacements[key])

	return alter
