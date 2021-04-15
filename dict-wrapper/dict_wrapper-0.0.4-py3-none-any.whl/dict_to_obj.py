class DictWrapper:

    class Dict(dict):
        __setattr__ = dict.__setitem__
        __getattr__ = dict.__getitem__

    @staticmethod
    def wrapper(dictionary):
        if isinstance(dictionary, list):
            array_obj = []
            for item in dictionary:
                array_obj.append(DictWrapper.wrapper(item))
            return array_obj
        if not isinstance(dictionary, dict):
            return dictionary
        obj = DictWrapper.Dict()
        for k, v in dictionary.items():
            obj[k] = DictWrapper.wrapper(v)
        return obj

    def __new__(cls, *args, **kwargs):
        return DictWrapper.wrapper(args[0])

DW = DictWrapper

if __name__ == '__main__':
    data = {
        "who": 'your name',
        "area": ['specify', 'china'],
        "province": {
            "city": ['shenzhen', 'guangzhou']
        },
        "citys":[{
            "name":"shenzhen",
            "othername":"鹏城"
        }]
    }
    config, config1 = DW(data), DictWrapper(data)
    assert config.who == 'your name'
    assert config.province.city == ['shenzhen', 'guangzhou']
    print(config.area)
    print(config1.citys[0].name)
