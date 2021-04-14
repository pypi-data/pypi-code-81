import os

import requests

from tensorfn.checker.backend import Backend, torch_serialize


class Nubes(Backend):
    def __init__(
        self, bucket, path_format, lookup="http://a-dev.lookup.nubes.navercorp.com:8080"
    ):
        self.bucket = bucket
        self.gateway = self.get_gateway(lookup)
        self.path = self.get_directory(path_format)

    def get_gateway(self, lookup):
        url = requests.get(f"{lookup}/v1/address").text

        return f"http://{url}"

    def list(self, directory="/"):
        results = []
        token = ""
        finished = False

        target = f"{self.gateway}/v1/{self.bucket}"

        while not finished:
            params = {
                "dir": directory,
                "max-contents": 100,
                "continuation-token": token,
            }
            response = requests.get(target, params=params)

            if not response.ok:
                response.raise_for_status()

            fetched = response.json()
            results.extend(fetched)

            if len(fetched) == int(response.headers["X-Content-Counter"]):
                break

            token = response.headers["X-Continuation-Token"]

        return results

    def get_duplicates(self, path):
        dirs = self.listdir(os.path.split(path)[0])
        dups = [d for d in dirs if d.startswith(os.path.split(path)[-1])]

        return dups

    def listdir(self, directory="/"):
        return [i["Name"] for i in self.list(directory)]

    def save(self, content, name, overwrite=True):
        path = os.path.join(self.path, name)
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


class NSML:
    def bind(self, save_fn, load_fn):
        def save_wrapper(name):
            save_fn(os.path.join(name, "checkpoint"))

        nsml.bind(save=save_wrapper, load=load_fn)

    def save(self, name):
        nsml.save(name)

    def log(self, step, **kwargs):
        nsml.report(summary=True, step=step, **kwargs)


backends = {"nsml": NSML, "nubes": Nubes}

