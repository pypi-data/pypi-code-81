from lazy import lazy

from benchmark.storage import pickledb_adapter


class Storage(object):

    @property
    def config(self):
        return self._config

    def __init__(self, c) -> None:
        self._config = c
        self._adapter_name = self.config.storage_name()
        self._adapter = None

    @lazy
    def adapter(self):
        if self._adapter_name == "pickledb":
            return pickledb_adapter.PickledbAdapter(self.config)

    def set(self, key, data):
        self.adapter.set(key, data)
        self.adapter.dump()

    def set_list_of_benches_results(self, bench_results):
        for item in bench_results:
            bench_name = item.get("benchmark_name")
            list_results = self.adapter.get_list(bench_name)
            list_results.append(item)

        self.adapter.dump()

    def get(self, key):
        return self.adapter.get(key)

    def get_list_all(self):
        bench_names = self.adapter.getall()
        l = []
        for key in bench_names:
            l.append({
                'name': key,
                'data': self.adapter.get_list(key)
            })
        return l
