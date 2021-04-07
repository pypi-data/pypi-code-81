
from swissarmykit.conf import *

from swissarmykit.db.mongodb import BaseDocument
from swissarmykit.utils.dateutils import DateUtils


class CacheMongoDB:

    def __init__(self):
        self.p = None

    def get(self, key):
        obj = self.p.get_by_url(key)
        return obj.value if obj else None

    def get_start_withs(self, key):
        return self.p.get_one(-1, filters={'url__startswith': key})

    def get_lastest(self, key):
        obj = self.p.get_one_item(filters={'url__startswith': key}, order_by=['-order_by'])
        return obj.value if obj else None

    def set(self, key, value, attr=None):
        return self.p.save_url(key, value=value, attr=attr, update_modified_date=True)

    def save_attr(self, key, attr=None):
        return self.p.save_url(key, attr=attr, update_modified_date=True)

    def clean(self):
        for item in self.p.get_one(-1, filters={'updated_at__lte': DateUtils.datetime_second_diff(86400)}): # 24 hour
            item.delete()

    def dump_object(self, key, value, attr=None):
        return self.p.save_url(key, value=value, attr=attr, update_modified_date=True)

    def load_object(self, key):
        return self.p

@Singleton
class Preferences(CacheMongoDB):

    def __init__(self):
        super().__init__()
        self.p = BaseDocument.get_class('preferences', db_name='meta')

    def get(self, key):
        return self.p.get_by_url(key).value

    def set(self, key, value, attr=None):
        return self.p.save_url(key, value=value)

    def __str__(self):
        return 'Preferences: For settings global data like Redis'

@Singleton
class ProcessLog(CacheMongoDB):

    def __init__(self):
        super().__init__()
        self.p = BaseDocument.get_class(swissarmykit_conf.config.get('meta_db', 'meta') + '.process_log')

    def __str__(self):
        return 'ProcessLog: For process tmp checkpoint like Redis'


@Singleton
class ProcessTmp(CacheMongoDB):

    def __init__(self):
        super().__init__()
        self.p = BaseDocument.get_class('process_tmp', db_name='meta')

    def __str__(self):
        return 'ProcessTmp: For process tmp checkpoint like Redis'

@Singleton
class OtherProcessTmp(CacheMongoDB):

    def __init__(self):
        super().__init__()
        self.p = BaseDocument.get_class('process_tmp', db_name='meta', other_db=True)

    def __str__(self):
        return 'OtherProcessTmp: For process tmp checkpoint like Redis'

if __name__ == '__main__':
    # p = ProcessTmp.instance()
    p = OtherProcessTmp.instance()
    # d = p.set('test', 3)
    # print(DateUtils.datetime_second_diff(10)) # 1588289813002

    # FileUtils.dump_object_to_file()
    print(p)


