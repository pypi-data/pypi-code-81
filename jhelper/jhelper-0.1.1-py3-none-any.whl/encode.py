from requests import get
from random import choice
import string
import time
from io import BytesIO
from pathlib import Path
from hashlib import md5


def random_str():
    return "".join([choice(string.ascii_letters) for _ in range(5)])


def get_image():
    resp = get(
        "https://api.deepai.org/api/text2img",
        headers={"api-key": "9cf43c72-43c0-49db-8c20-c94b5c54093d"},
        data={"text": random_str()},
    )
    img_url = resp.json()["output_url"]
    resp = get(img_url)
    return resp.content
    # return to_png(resp.content)


def to_md5(timestamp):
    inst = md5()
    inst.update(str(timestamp).encode("utf-8"))
    return inst.hexdigest().encode("utf-8")


def encode_file(encode, fp):
    if not encode:
        return (fp.name, BytesIO(fp.read()))
    outfile = BytesIO()
    outfile.write(get_image())
    timestamp = int(time.time())
    outfile.write(to_md5(timestamp))
    outfile.write(fp.read())
    outfile.seek(0)
    return (f"sample_image_{timestamp}.jpg", outfile)


def encode_dir(dirpath):
    chunks = [chunk for chunk in Path(dirpath).iterdir()]
    chunks.sort(key=lambda x: x.name)
    for chunk in chunks:
        if chunk.name != "fs_manifest.csv":
            fname, encoded = encode_file(True, chunk.open("rb"))
            with open(f"encoded/{fname}", "wb") as f:
                f.write(encoded.read())
