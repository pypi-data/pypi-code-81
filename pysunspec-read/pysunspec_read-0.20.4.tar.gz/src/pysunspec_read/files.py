def check_filename_ends_with_json(output_file_path):
    check_ends_with(".json", output_file_path)


def check_ends_with(extension, output_file_path):
    if not str(output_file_path).endswith(extension):
        expected_message = "output path must end with {ext} for example " \
                           "c:/output/reading{ext} or /home/output/reading{ext}".format(ext=extension)
        raise ValueError(expected_message)
