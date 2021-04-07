from swissarmykit.db.mongodb import BaseDocument

try: from definitions_prod import *
except Exception as e: pass

class OtherBaseDocument(BaseDocument):

    meta = {
        'abstract': True,
        'db_alias': appConfig.get_connect_to_other_mongodb()
    }

    _db_alias = appConfig.get_connect_to_other_mongodb()

if __name__ == '__main__':
    o = OtherBaseDocument()

