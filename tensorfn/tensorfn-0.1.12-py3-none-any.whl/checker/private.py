import requests


class Nubes:
    def __init__(self, bucket, lookup="http://a-dev.lookup.nubes.navercorp.com:8080"):
        self.bucket = bucket
        self.gateway = self.get_gateway(lookup)

    def get_gateway(self, lookup):
        url = requests.get(f"{lookup}/v1/address").text

        return f"http://{url}"

    def put(self, path, content, overwrite=False):
        target = f"{self.gateway}/v1/{self.bucket}/{path}"
        headers = {
            "Content-Length": str(len(content)),
            "Content-Type": "application/octet-stream",
        }
        params = {"overwrite": overwrite}

        response = requests.post(target, data=content, headers=headers, params=params)

        if not response.ok:
            response.raise_for_status()

        return response.headers
