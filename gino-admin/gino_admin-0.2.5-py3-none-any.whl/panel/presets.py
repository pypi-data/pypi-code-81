import yaml


def create_preset_file(
    preset_file_path,
):
    with open(preset_file_path, "w+") as p_file:
        yaml.dump(data, stream)
