
## https://docs.python.org/2/library/collections.html. Counter, DefaultDict

class Dict(dict):

    def __init__(self, default=None):
        self.default = default
        super().__init__()

    def sort(self, reverse=False, sort_by_key=False):
        sort_by = 0 if sort_by_key else 1
        return {k: v for k, v in sorted(self.items(), key=lambda item: item[sort_by], reverse=reverse)}

    def sort_asc(self, sort_by_key=False):
        return self.sort(reverse=True, sort_by_key=sort_by_key)

    def add(self, key, value=1):
        self[key] = value

    def count(self, key):
        if key not in self:
            self[key] = 0
        self[key] = self.get(key) + 1

    def append(self, key, value):
        if key not in self:
            self[key] = self.default.copy()
        self[key].append(value)

    def get_keys(self):
        return list(self.keys())

    def get_values(self):
        return list(self.values())

if __name__ == '__main__':
    data = Dict()

    data['test5'] = 5
    data['test6'] = 6
    data['test1'] = 1
    data['test9'] = 9

    print(data.sort(reverse=True, sort_by_key=False))
