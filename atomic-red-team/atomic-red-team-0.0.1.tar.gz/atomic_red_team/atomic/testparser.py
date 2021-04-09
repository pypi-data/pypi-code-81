class TestParser:

    def parse(self, item):
        for key,val in item.items():
            if hasattr(self, key):
                if not isinstance(getattr(self, key), list):
                    v = getattr(self, key)
                    setattr(self, key, [v])
                v = getattr(self, key)
                v.append(val)
                setattr(self, key, v)
            if not hasattr(self, key):
                setattr(self, key, val)
        return self
