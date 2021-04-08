import yaml
import os

class Model(dict):
    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

class Secrets(Model):
    def __init__(self, path="secrets"):
        self.path = path
        self.f = None
        self.d = {}

        with open(".gitignore", "a+") as f:
            f.seek(0)
            for line in f:
                if path == line.strip("\n"):
                    break
            else:
                f.write(path + '\n')

        if os.path.exists(path):
            with open(path, 'r') as f:
                self.d = yaml.load(f, Loader=yaml.FullLoader)

    def save(self):
        with open(self.path, 'w') as f:
            yaml.dump(self.d, f)

    def __getitem__(self, key):
        return self.d[key]

    def __setitem__(self, key, value):
        self.d[key] = value
        self.save()

