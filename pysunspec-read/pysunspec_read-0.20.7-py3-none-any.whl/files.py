def filename_ends_with_json(output_file_path) -> bool:
    return ends_with(".json", output_file_path)


def ends_with(extension, output_file_path) -> bool:
    return str(output_file_path).endswith(extension)
