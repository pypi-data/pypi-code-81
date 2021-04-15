import toml


def path_to_bytes(path: str) -> bytes:
    data = open(path, "rb")
    return data.read()


def dict_to_bytes(config: dict) -> bytes:
    json_string = toml.dumps(config)
    return json_string.encode()