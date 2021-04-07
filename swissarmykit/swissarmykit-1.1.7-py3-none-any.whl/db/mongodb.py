# from swissarmykit.db.datatables import DataTables

import json
import os
import sys
import csv
from pprint import pprint
from typing import List, Union, Tuple
from datetime import datetime
from mongoengine.base import UPDATE_OPERATORS
from mongoengine import *
from pymongo import UpdateOne, InsertOne

from swissarmykit.conf import *

from swissarmykit.utils.dateutils import DateUtils
from swissarmykit.utils.timer import Timer
from swissarmykit.req.FileThread import FileTask
from swissarmykit.utils.fileutils import FileUtils
from swissarmykit.utils.stringutils import StringUtils
from swissarmykit.utils.counter import Counter
from swissarmykit.utils.command import Command
from swissarmykit.office.excelutils import ExcelUtils
from urllib.parse import parse_qs, urlparse

from mongoengine.queryset.visitor import Q as MQ
from mongoengine.queryset.visitor import QCombination



class BaseDocument(DynamicDocument):
    '''
        url = StringField(sparse=True, required=True, unique=True)
        name = StringField()
        has_html_1 = BooleanField()
        data = DictField()
        extra = DictField()
        images = StringField()
        version = IntField()
        updated_at = DateTimeField(default=datetime.now)

        SQL Terms/Concepts	    MongoDB Terms/Concepts
        database	            database
        table	                collection
        row	                    document or BSON document
        column	                field
        index	                index
        table joins	            $lookup, embedded documents
        primary key             primary key

        Field define: http://docs.mongoengine.org/guide/defining-documents.html
    '''
    meta = {
        'abstract': True,
    }

    _db_alias = 'default'
    _db_name = None
    _html_path = None
    _check_html_exists = True
    _check_is_insert = False


    url = StringField(sparse=True, required=True, unique=True)
    name = StringField()
    has_html_1 = BooleanField()
    deleted = BooleanField(default=False)
    data = DictField()
    value = DynamicField()
    extra = DictField()
    images = StringField()
    version = IntField()
    counter = IntField(min_value=0, default=0)
    updated_at = DateTimeField(default=datetime.now)

    timer = None
    is_tmp = False
    cur_level = 1
    _counter = Counter.instance()

    @classmethod
    def get_db(cls, db_name="default"):
        return get_db(db_name)

    @classmethod
    def get_db_name(cls):
        return cls._db_name if cls._db_name else FileUtils.conf.DATABASE_NAME

    @classmethod
    def get_meta(cls):
        return cls._meta

    @classmethod
    def count(cls, filters=None):  # type: (dict) -> int
        if filters:
            cls.objects.filters(**filters).count()
        return cls.objects.count()

    @classmethod
    def delete_html(cls, id=None, lst=None, level=1):
        has_html_ = {'unset__has_html_%d' % level: 1}
        if id:
            cls.objects(id=id).update(**has_html_)
        if lst:
            cls.objects.filter(**{'id__in': lst}).update(**has_html_)
        raise Exception('Cls required id, and lst')

    @classmethod
    def inc_counter(cls, val, col='id', as_obj=False):
        obj = cls.objects(**{col:val})
        if obj:
            obj.update(inc__counter=1)
            if as_obj:
                return obj.first()
            return obj.first().counter
        return 0

    def increment(self):
        self.update(inc__counter=1)
        return self.counter + 1

    def remove_html(self, level=1):
        self.update(**{'unset__has_html_%d' % level: 1})

    @classmethod
    def delete_table(cls):
        cls.drop_collection()

    @classmethod
    def truncate_table(cls):
        cls.drop_collection()

    @classmethod
    def exists_id(cls, id):
        return cls.objects.with_id(object_id=id)

    @classmethod
    def exists(cls, col: str, val):
        return True if cls.objects(__raw__={col: val}) else False

    @classmethod
    def get_all_rows(cls):
        return [o for o in cls.objects]

    @classmethod
    def get_all_docs(cls):
        return [o for o in cls.objects]

    @classmethod
    def exists_html(cls, url, level=1):
        has_html_ = 'has_html_%d' % level
        return getattr(cls.get_by_url(url), has_html_)

    @classmethod
    def dump_mysql_of_this_table(cls, path=None):
        lst = [o.to_json() for o in cls.objects]
        FileUtils.to_html_file(path, json.dumps(lst))

    @classmethod
    def get_first_row(cls):  # type: () -> BaseDocument
        return cls.objects.first()

    @classmethod
    def get_items(cls, **kwargs):  # type: (any) -> []
        if 'limit' not in kwargs: kwargs['limit'] = - 1
        return [item for item in cls.get_one(**kwargs)]

    @classmethod
    def get_record(cls, **kwargs):  # type: (dict) -> BaseDocument
        return cls.get_one(limit=1, **kwargs)

    @classmethod
    def get_records(cls, **kwargs):  # type: (dict) -> Union[List[BaseDocument], BaseDocument]
        return cls.get_one(limit=-1, **kwargs)

    @classmethod
    def print_database_info(cls):
        print('Database: %s. Table: %s\nMeta: %s' % (cls.get_db_name(), cls.get_table_name(), str(cls.get_meta())))

    @classmethod
    def get_all_schemas(cls):
        return cls.get_db().adminCommand('listDatabases')

    @classmethod
    def show_tables(cls):
        pprint(cls.get_all_collection_name())

    @classmethod
    def get_all_tables(cls):
        return cls.get_all_collection_name()

    @classmethod
    def get_table_name(cls):
        return cls._get_collection_name()

    @classmethod
    def get_collection_name(cls):
        return cls._get_collection_name()

    @classmethod
    def get_all_collection_name(cls):
        return cls.get_db(cls._db_alias).list_collection_names()

    @classmethod
    def insert_record(cls, data=None):
        return cls(**data).save()

    @classmethod
    def get_fields(cls):
        field_dict = cls.get_first_row()._fields
        lst = []
        for field_name, field in field_dict.items():
            lst.append(field_name)
            # print(field_name, field.required, field.__class__)
        return lst

    @classmethod
    def export_data_to_csv_2(cls, lst=None, headers_order=None, col_name='data', limit=-1, offset=0,
                             headers=None, callback_format_data=None,
                             remove_invalid_char=False, auto_order_header=False, sort_header=None,
                             file_name=None):

        file = FileUtils.conf.EXCEL_PATH + '/' + (file_name if file_name else cls.get_collection_name()) + '.csv'

        with open(file, 'w', newline='', encoding="utf-8") as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

            if not headers:
                print('INFO: Will automatic get headers')
                headers = cls.get_headers()

            wr.writerow(headers)

            if not lst:
                lst = cls.get_one(limit=limit, offset=offset, col_name=col_name, is_null_data=False) if col_name == 'data' else cls.get_one(
                    limit=limit, offset=offset, col_name=col_name)

            for item in lst:
                try:
                    item.check()

                    data = item.get_data()
                    if callback_format_data:
                        data = callback_format_data(data)

                    _l = []

                    for h in headers:
                        _l.append(data.get(h, ''))
                    wr.writerow(_l)
                except Exception as e:
                    print('Error: Retry ', e, ' data:', _l, ' line: ', item.get_id_offset())
                    try:
                        wr.writerow([StringUtils.get_valid_utf_8(__l) for __l in _l])
                    except Exception as e:
                        print('error:', e, ' SKIP')

    @classmethod
    def export_data_to_csv(cls, lst=None, headers=None, file_name=None):
        file = FileUtils.conf.EXCEL_PATH + '/' + (file_name if file_name else cls.get_collection_name()) + '.csv'
        print('INFO: Total: ', len(lst))
        if isinstance(lst[0], dict):
            lst = [list(item.values()) for item in lst]

        if headers:
            lst.insert(0, headers)

        timer = Timer.instance()
        timer.reset(len(lst))
        with open(file, 'w', newline='', encoding="utf-8") as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for i, l in enumerate(lst):
                try:
                    timer.check(idx=i)
                    wr.writerow(l)
                except Exception as e:
                    print('Error: Retry ', e, ' data:', l, ' line: ', i + 1)
                    try:
                        wr.writerow([StringUtils.get_valid_utf_8(_l) for _l in l])
                    except Exception as e:
                        print('error:', e, ' SKIP')
        print('INFO: Output to CSV ', file)

    @classmethod
    def convert_excel_to_csv(cls):
        pass

    @classmethod
    def export_data_to_excel(cls, lst=None, headers_order=None, col_name='data', limit=-1, offset=0, format='',
                             headers=None, callback_format_data=None,
                             remove_invalid_char=False, debug=False, auto_order_header=False, sort_header=None,
                             file_name='', write_one_by_one=False):
        '''

        :param lst:
        :param headers_order: Header order base on few order
        :param col_name:
        :param limit:
        :param offset:
        :param format:
        :param headers: Header limit exectly
        :param callback_format_data:
        :param remove_invalid_char:
        :param debug:
        :param auto_order_header:
        :param sort_header:
        :param file_name:
        :param write_one_by_one:
        :return:
        '''
        data_lst = []
        if lst is not None:
            data_lst = lst[offset:limit] if limit > 0 else lst[offset:]
        else:
            __lst = cls.get_one(limit=limit, offset=offset, col_name=col_name, is_null_data=False) if col_name == 'data' else cls.get_one(limit=limit,
                                                                                                                                          offset=offset,
                                                                                                                                          col_name=col_name)
            for item in __lst:
                try:
                    data = getattr(item, col_name)
                    if remove_invalid_char:
                        data = {k: StringUtils.get_valid_text_for_excel(v) for k, v in data.items()}

                    if callback_format_data:
                        data = callback_format_data(data, item)
                        if not data:
                            continue
                    data_lst.append(data)
                except Exception as e:
                    print('ERROR: ', e, item)

        # Auto get header_order
        if auto_order_header or headers_order:
            headers = {}
            for data in data_lst:
                for key in data.keys():
                    headers[key] = 1
            new_order = list(headers.keys())

            if sort_header:
                if sort_header in ['DESC', 'desc']:
                    new_order.sort(reverse=True)
                else:
                    new_order.sort()

            if headers_order:
                headers = {}
                headers_order = headers_order + new_order
                for key in headers_order: headers[key] = 1
                headers_order = list(headers.keys())
            else:
                headers_order = new_order

        if debug:
            print(data_lst)

        if not data_lst:
            print('ERROR: Empty list to export to Excel')
            return False

        if not file_name:
            file_name = FileUtils.conf.EXCEL_PATH + '/' + cls.get_collection_name() + '.xlsx'

        ExcelUtils.json_to_openpyxl(data_lst, headers_order=headers_order, headers=headers, file_name=file_name,
                                    write_one_by_one=write_one_by_one)

    @classmethod
    def export_header_key(cls, col_name='data'):
        headers = {}
        for item in cls.objects:
            data = getattr(item, col_name)

            if data:
                for h in data.keys():
                    headers[h] = 0
        re = list(headers.keys())
        print(re)
        return re

    def get_values(self):
        lst = []
        fields = self.get_fields()
        data = self.__dict__.get('_data')
        for f in fields:
            lst.append(data.get(f) if data.get(f) else '')
        return lst

    @classmethod
    def output_html(cls, id=None, path=None):
        item = cls.objects(id=id)
        path = path if path else FileUtils.conf.USER_DESKTOP + '/_test_html.html'
        FileUtils.to_html_file(path, item.get_html())
        print('INFO: output to html of %d:%s' % (id, path))

    @classmethod
    def get_html_by_id(cls, id=1, output=False):
        item = cls.get_html_by_id(id)
        html = item.get_html()
        if output:
            html_path = '%s/%s_id_%d.html' % (FileUtils.conf.get_desktop_path(), cls.get_collection_name(), id)
            FileUtils.to_html_file(html_path, html)
            print('INFO: output to html: %s' % html_path)

        return html

    @classmethod
    def get_by_url(cls, url):  # type: (str) -> (BaseDocument or None)
        try:
            return cls.objects.get(url=url)
        except Exception as e:
            # print('ERROR: ', e)
            return None

    @classmethod
    def get_by_id(cls, id):  # type: (str) -> (BaseDocument or None)
        try:
            return cls.objects.get(id=id)
        except Exception as e:
            # print('ERROR: ', e)
            return None

    @classmethod
    def get_html_by_url(cls, url):  # type: (str) -> str
        item = cls.get_by_url(url)
        if item:
            return item.get_html()
        return ''

    @classmethod
    def get_counter(cls):  # type: () -> Counter
        return cls._counter

    @classmethod
    def get_urls(cls, have_html=None):
        if have_html:
            return cls.objects.filter(**{'has_html_1': True}).values_list('url')

        return cls.objects.values_list('url')

    @classmethod
    def get_headers(cls, remove=(), remove_contains=(), col_name='data', limit=-1):
        headers = {}

        timer = Timer.instance()
        timer.reset(cls.count())

        qs = cls.objects
        if limit > 0:
            qs = qs.limit(limit)

        for o in qs:
            timer.check()

            data = getattr(o, col_name)
            if not data:
                continue

            for h in data:
                if h not in headers:
                    headers[h] = 1

        new_headers = {}
        for h in headers:
            if h in remove:
                continue
            skip = False
            for c in remove_contains:
                if c in h:
                    skip = True
            if skip:
                continue

            new_headers[h] = 1
        return list(new_headers.keys())

    @classmethod
    def get_ids(cls):
        return [str(o.id) for o in cls.objects.only(*['id'])]

    @classmethod
    def exists_url(cls, val, is_cache=True):
        '''
        Cache get_all_urls as default. Improve performance

        :param val: url
        :param is_cache: default all
        :return:
        '''
        if is_cache:
            if not hasattr(cls, '__cache_url'):
                setattr(cls, '__cache_url', frozenset(cls.get_urls()))
                # print(hex(id(cls)))

            return val in getattr(cls, '__cache_url')

        return cls.exists('url', val)

    @classmethod
    def find_by_url(cls, url):
        return cls.get_by_url(url)

    @classmethod
    def save_url(cls, url, name=None, html=None, data=None, value=None, extra=None, attr=None, level=1, update_modified_date=None,
                 force_insert=False, setOnInsert=None):  # type: (str, str, str, dict, any, dict, dict, int, bool, bool, dict) -> BaseDocument

        # if not cls.is_tmp and '?' in url:
        #     print('WARN: should strip ? for unique url')

        if not url:
            return 0

        _data = {'url': url}
        if name:
            _data['name'] = name
        if data:
            _data['data'] = data
        if value:
            _data['value'] = value

        if extra:
            _data['extra'] = extra

        if update_modified_date:
            _data['updated_at'] = datetime.now()

        if attr:
            _data.update(attr)

        if setOnInsert:
            for k, v in setOnInsert.items():
                if k not in _data:
                    _data['set_on_insert__%s' % k] = v
        try:
            _is_new = False
            if force_insert:
                obj = cls(**_data).save()
                _is_new = True
            else:
                if cls._check_is_insert: _is_new = not cls.exists_url(url)
                obj = cls.objects(url=url).upsert_one(write_concern=None, **_data)

            if cls._check_is_insert: obj._is_new = _is_new

        except Exception as e:
            cls.valid_data(_data)
            print(f'ERROR: {url}', _data)
            raise e

        if html:
            obj.save_html(html, level)

        return obj

    @classmethod
    def create(cls, attr, category='default'): # type: (dict, str) -> BaseDocument
        try:
            attr['category'] = category
            return cls(**attr).save()
        except Exception as e:
            print(f'ERROR: ', attr)
            raise e

    @classmethod
    def bulk_update(cls, lst, key='id'):
        ''' Bulk update by id or url '''

        bulk_operations = []

        for data in lst:
            try:
                k = '_id' if key == 'id' else key # key: _id or id
                if k == '_id':
                    k_val = data.get('id' if 'id' in data else '_id')
                else:
                    k_val = data.get(k)

                bulk_operations.append(UpdateOne({k: k_val}, {'$set': data}))
            except Exception as e:
                print('Exception: ', e)

        if bulk_operations:
            return cls._get_collection().bulk_write(bulk_operations, ordered=False)

        return None


    @classmethod
    def bulk_insert(cls, lst):
        bulk_operations = []

        for data in lst:
            try:
                bulk_operations.append(cls(**data))
            except Exception as e:
                print('Exception: ', e)

        if bulk_operations:
            return cls.objects.insert(bulk_operations)

        return None

    def is_new(self):
        return self._is_new

    @classmethod
    def get_last(cls):
        return cls.objects.order_by('-id').first()

    @classmethod
    def get_one_item(cls, **kwargs):
        if 'limit' in kwargs: del kwargs['limit']
        # print('get_one_item', kwargs)
        return cls.get_one(limit=1, **kwargs).first()

    @classmethod
    def get_one(cls, limit: int = 1, offset: int = 0, col_name: Union[list,str] = None, desc: bool = None, where_id: any = None, where_url: any = None,
                where_url_contains: str = None,
                filters: dict = None, filters_combination:any=None, order_by=None, have_html=None, level=1,
                is_null_data: bool = None, is_null_extra: bool = None, ago: str = None, ago_gte: str = None, from_time:str = None,
                no_cursor_timeout: bool = False, timeout: int = False, batch_size: int = 0) -> Union['BaseDocument', QuerySet, List['BaseDocument']]:
        '''
        Query builder.

        https://docs.python.org/3/library/typing.html
        http://docs.mongoengine.org/guide/querying.html
            result exhausation
            batchSize:
            timeout: alias with no_cursor_timeout
        '''

        cls._counter.offset = offset
        cls.cur_level = level
        filter = filters if filters else {}

        if where_id:
            if isinstance(where_id, list):
                filter['id__in'] = where_id
            else:
                filter['id'] = where_id

        if where_url_contains:
            filter['url__icontains'] = where_url_contains

        if where_url:
            if isinstance(where_url, list):
                filter['url__in'] = where_url
            else:
                filter['url'] = where_url

        if have_html is not None:
            if have_html:
                filter['has_html_%s' % level] = True
            else:
                filter['has_html_%s' % level] = None

        if is_null_data is not None:
            if is_null_data:
                filter['data'] = None
            else:
                filter['data__ne'] = None

        if is_null_extra is not None:
            if is_null_extra:
                filter['extra'] = None
            else:
                filter['extra__ne'] = None

        if from_time:
            diff = DateUtils.get_current_time_str()

        if ago:
            diff = DateUtils.get_diff_ago(ago)
            if diff:
                filter['updated_at__lte'] = diff

        if ago_gte:
            diff = DateUtils.get_diff_ago(ago_gte)
            if diff:
                filter['updated_at__gte'] = diff

        if filters_combination:
            qs = cls.objects(filters_combination).filter(**filter)
            # print('filters_combine', filters_combine)
        else:
            qs = cls.objects.filter(**filter)
            # print('get_one', filter)

        if col_name:
            if isinstance(col_name, str):
                qs = qs.only(*[col_name])
            else:
                qs = qs.only(*col_name)

        if desc is not None:
            if desc:
                qs = qs.order_by('-id')
            else:
                qs = qs.order_by('+id')

        if order_by:
            if isinstance(order_by, str):
                qs = qs.order_by(*[order_by])
            elif isinstance(order_by, list):
                qs = qs.order_by(*order_by)
            else:
                qs = qs.order_by(**order_by)

        if offset:
            qs = qs.skip(offset)  # Skip is expensive . https://stackoverflow.com/questions/13935733/mongoose-limit-offset-and-count-query

        if limit > 0:
            qs = qs.limit(limit)

        if no_cursor_timeout or batch_size or not timeout:
            qs = qs.timeout(False)  # not work yet

        if batch_size:
            qs = qs.batch_size(batch_size)

        # print(qs.explain())

        _t = qs.count() - offset
        cls.timer = Timer.instance()
        cls.timer.reset(_t)

        # if not _t: print('WARNING: Records in db ', cls.count(), ', Count(*): 0, Current offset: ', offset)
        return qs

    def check(self):
        ''' Check timer '''
        self._counter.count_offset()
        if self.timer:
            self.timer.check(self, idx=self._counter.offset)
        return self._counter.offset

    def _get_offset(self):
        return self._counter.offset

    def save_html(self, html, level=1, update_modified_date=None):  # type: (str, int, bool) -> BaseDocument
        if not html: return 0

        if FileTask(id=self.id, table=self.get_collection_name(), html=html, html_path=self.get_html_path()).save(level=level):
            update = {'has_html_%d' % level: True}
            if update_modified_date:
                update['updated_at'] = datetime.now()

            return self.update(**update)
        return False

    @classmethod
    def get_html_path(cls):
        return cls._html_path

    def get_html(self, level=1, unset_html=False, set_warn_msg=True, encoding='utf-8'):  # type: (int, bool, bool, str) -> str
        self.check()
        if self.cur_level != 1:
            level = self.cur_level

        try:
            if self._check_html_exists and not getattr(self, 'has_html_%d' % level):
                raise Exception('Not found html')

            return FileTask(id=self.id, table=self.get_collection_name(), html_path=self.get_html_path(), encoding=encoding).load(level=level)
        except Exception as e:
            if unset_html:
                print(' d ', end='', flush=True)
                self.remove_html(level=level)
                raise e

        if set_warn_msg: print('WARNING: Not found html, id', self.id)
        return ''

    def copy_to_clipboard(self, level=1, is_print=True):
        html = self.get_html(level=level)
        if is_print:
            StringUtils.copy(html)
            print('INFO: copy html to clip board')

    def check_html_value(self, level=1):
        try:
            if self.have_html_file(level=level):
                self.save_attr({'has_html_%d' % level: True})
                return True
        except Exception as e:
            print('ERROR: ', e)
        return False

    def have_html(self, level=1, unset_html=False):
        try:
            if getattr(self, 'has_html_%d' % level):
                if FileTask(id=self.id, table=self.get_collection_name(), html_path=self.get_html_path()).exists(level=level):
                    return True
        except Exception as e:
            print('ERROR: ', e)

        if unset_html:
            print('.', end='', flush=True)
            self.remove_html(level=level)

        return False

    def have_html_file(self, level=1):
        return FileTask(id=self.id, table=self.get_collection_name(), html_path=self.get_html_path()).exists(level=level)

    def get_url_query(self):
        return parse_qs(urlparse(self.url).query)

    def get_html_size(self, level=1):
        '''

        :param level:
        :return: int bytes
        '''
        if getattr(self, 'has_html_%d' % level):
            return FileTask(id=self.id, table=self.get_collection_name(), html_path=self.get_html_path()).size(level=level)

        print('WARNING: Not found html, id', self.id)
        return 0

    def save_extra(self, data):
        return self.update(**{'extra': data})

    def save_name(self, name):
        return self.update(**{'name': name})

    def get_extra(self):
        return self.extra

    def get_id_offset(self):
        return self._counter.offset

    @classmethod
    def get_offset(cls, url):
        urls = cls.get_urls()
        return urls.index(url)

    @classmethod
    def valid_data(cls, data):
        if set(data.keys()) & set(UPDATE_OPERATORS):
            raise Exception('ERROR: From MyApp: keys must not same as ' + str(data.keys()) + ' - ' + str(UPDATE_OPERATORS))
        return True

    def save_data(self, data, value=None, attr=None, update_modified_date=None, setOnInsert=None):  # type: (dict, any, dict, bool, dict) -> BaseDocument
        update = {'data': data} if data else {}

        if update_modified_date:
            update['updated_at'] = datetime.now()
        if value:
            update['value'] = value

        if attr:
            update.update(attr)

        try:
            if update:
                return self.update(**update)
            else:
                print('ERROR: Update, but no data to update')
        except Exception as e:
            self.valid_data(update)
            raise e
        return None

    def remove_data(self):
        self.update(**{'unset__data': 1})

    def save_attr(self, attr, value=None, update_modified_date=None, setOnInsert=None):
        self.save_data(None, attr=attr, value=value, update_modified_date=update_modified_date, setOnInsert=setOnInsert)
        return self

    def save_value(self, value):
        self.save_data({}, value=value)

    def get_data(self):
        return self.data

    @classmethod
    def find_one_by_id(cls, id):  # type: (int) -> BaseDocument
        return cls.objects.get(id=id)

    @classmethod
    def get_all(cls, col_name=None, filters=None, to_json=False, **kwargs):
        # type: (List[str], dict, bool, dict) -> Union[List[BaseDocument], BaseDocument, List[dict]]
        limit = -1
        if 'limit' in kwargs:
            limit = kwargs.get('limit')
            del kwargs['limit']
            
        if to_json:
            return [i.get_json() for i in cls.get_one(limit, col_name=col_name, filters=filters, **kwargs)]
        return cls.get_one(limit, col_name=col_name, filters=filters, **kwargs)

    @classmethod
    def output_tmp(cls, id=1):
        return cls.output_html_by_id(id, FileUtils.conf.DIST_PATH + '/tmp.html')

    @classmethod
    def output_html_by_id(cls, id=1, html_path=None):
        item = cls.get_one(where_id=id)
        html = item.get_html()

        if not html_path:
            html_path = '%s/%s_id_%d.html' % (FileUtils.conf.get_desktop_path(), cls.get_table_name(), id)
        FileUtils.to_html_file(html_path, html)
        return html

    def set_data_null(self):
        self.delete_html(self.id)

    @classmethod
    def count_not_html(cls, level=1):
        return cls.get_one(-1, have_html=False, level=1).count()

    @classmethod
    def update_html_to_1(cls, value=True, level=1):
        print('INFO: set has_html_1 = ', value)

        if value:
            update = {'has_html_%d' % level: value}
        else:
            update = {'unset__has_html_%d' % level: 1}
        return cls.objects.update(**update)

    @classmethod
    def udpate_html_to_0(cls, level=1):
        cls.update_html_to_1(value=False, level=level)

    @classmethod
    def delete_all_html(cls):
        task = FileTask(0, cls.get_collection_name(), html_path=cls.get_html_path())
        task.delete_all()
        cls.udpate_html_to_0()
        print('INFO: Delete all folder %s' % task.get_path())

    @classmethod
    def get_tmp_class(cls, class_name='', level=1, other_db=False, db_name=None):  # type: (str, int, bool, str) -> BaseDocument
        class_name = 'zz_tmp_' + class_name + '_' + str(level)
        clazz = cls.get_class(class_name, other_db=other_db, db_name=db_name)
        clazz.is_tmp = True
        return clazz

    @classmethod
    def get_class(cls, class_name='', other_db=False, db_name=None, host=None, html_path=None, version=1, attributes=None):  # type: (str, bool, str, str, str, int, dict) -> BaseDocument
        '''
            other_db: attr for production.
            attributes: add more attributes. has_html_2: BooleanField(), etc...
        '''
        if '.' in class_name and class_name.count('.') == 1:
            db_name, class_name = class_name.split('.')


        if '.' in class_name and class_name.count('.') > 1:
            db_name, class_name, _host = class_name.split('.', 2)
            if _host.lower() == 'true':
                other_db = True
            else:
                if ':' not in _host: _host += ':27017'
                host = _host
            
        attributes = attributes if attributes else {}
        attributes['_html_path'] = html_path

        if db_name or other_db:
            # https://www.python-course.eu/python3_classes_and_type.php

            if not db_name: db_name = FileUtils.conf.DATABASE_NAME
            if other_db: host = FileUtils.conf.config.get('other_db').get('mongodb').get('host')

            _db_alias = FileUtils.conf.get_alias_mongodb(db_name, host)
            if other_db and not html_path: attributes['_html_path'] = FileUtils.conf.config.get('other_db').get('html_path')

            attributes.update({
                'meta': {
                    'db_alias': _db_alias
                },
                '_db_alias': _db_alias,
                '_db_name': db_name,
                '_check_html_exists': False if html_path else True
            })

            # noinspection PyTypeChecker
            class_: BaseDocument = type(class_name, (BaseDocument,), attributes)
            host = class_.get_cls_meta()
            if '127.0.0.1' not in host:
                print('INFO: Query from db_name ', host)
        else:
            # noinspection PyTypeChecker
            class_: BaseDocument = type(class_name, (BaseDocument,), attributes)

        return class_

    @classmethod
    def done_query(cls):
        print('BaseDocument: ', cls.get_collection_name(), '. Last offset: ', cls._counter.offset - 1)

    @classmethod
    def zip_data_to_desktop(cls):
        name = cls.get_collection_name()
        FileUtils.mkdir(FileUtils.conf.USER_DESKTOP + '/' + name)

        # html_path = FileTask(0, cls.get_collection_name()).get_path()
        # zip_name = '%s/%s/html_%s' % (FileUtils.conf.USER_DESKTOP, name, name)
        # FileUtils.zip_dir(zip_dir=html_path, zip_name=zip_name)

        program = '"C:/Program Files/MongoDB/Server/4.2/bin/mongodump.exe"'
        Command.exec(
            '%s --db %s --collection %s --gzip --archive > %s/%s/%s.gz' % (program, cls.get_db_name(), name, FileUtils.conf.USER_DESKTOP, name, name))

    @classmethod
    def sync_from_other(cls):
        pass

    @classmethod
    def sync_to_other(cls):
        pass

    @classmethod
    def print_all_row(cls):
        for row in cls.objects: print(row.to_json())

    def get_json(self, fields=None):  # type: (list) -> dict
        d = None
        if fields and 'data' in fields:
            fields.remove('data')
            d = self.get_data_log()

        data = self.to_mongo(fields=fields)
        data['id'] = str(data.pop('_id'))
        if 'updated_at' in data:
            data['updated_at'] = str(data.get('updated_at'))

        if d:
            data['data'] = d

        return dict(data)

    def get_data_log(self, fields=None):
        data = self.get_data()
        if not fields: fields = list(data.keys())

        d = {f: data.get(f, '') for f in fields}
        if '_id' in d:
            d['id'] = str(d.pop('_id'))
        if 'updated_at' in d:
            d['updated_at'] = str(d.get('updated_at'))
        return d

    def save_log(self, table='log', fields=None, extra=None, name='PUT'):
        data = self.to_mongo(fields=fields)
        collection_name = self.get_table_name()
        url = collection_name + '_' + str(data.get('_id')) + '_' + str(datetime.now()) + '_' + data['url']
        return BaseDocument.get_class(table).save_url(url, name=name, data=data, extra=extra, update_modified_date=True,
                                                      attr={'table': collection_name}, force_insert=True)

    def get_attr(self, fields=None):  # type: (list) -> dict
        return self.get_json(fields)

    def get_created_at(self):
        return self.id.generation_time()

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        if hasattr(self, 'url'):
            return '(%s %s)' % (str(self.id), getattr(self, 'url'))
        return str(self.id)

    @classmethod
    def clone_url_to_other(cls):
        other_cls = BaseDocument.get_class(cls.get_table_name(), other_db=True)
        for item in cls.get_one(-1, col_name='url'):
            other_cls.save_url(item.url)
            item.check()

    @classmethod
    def clone_to_other(cls):
        other_cls = BaseDocument.get_class(cls.get_table_name(), other_db=True)
        for item in cls.get_one(-1):
            other_cls.save_url(item.url, attr=item.to_mongo())
            item.check()

    @classmethod
    def duplicate_to(cls, table, limit=-1):
        new_table = BaseDocument.get_class(table)
        for item in cls.get_one(limit):
            obj = new_table(**item.to_mongo())
            obj.save()
            item.check()

    @classmethod
    def get_schema(cls, get_data_field=False):
        s_attr = set()
        s_data = set()

        for item in cls.get_one(10):
            a = item.get_json()
            if get_data_field and hasattr(item, 'data'):
                s_data.update(set(item.get_data()))

            s_attr.update(set(a.keys()))

        s_attr = list(s_attr)
        s_attr.remove('_id')

        if get_data_field:
            return s_attr, list(s_data)
        return s_attr

    @classmethod
    def crud_delete(cls, id, soft_detele=False):
        if soft_detele:
            cls.objects(id=id).update(deleted=True)
        else:
            cls.objects(id=id).delete()

    @classmethod
    def crud_restore(cls, id):
        item = cls.objects(id=id)
        if item:
            item.update(deleted=False)

    @classmethod
    def crud_update(cls, attr):  # type: (dict) -> any
        attr['updated_at'] = datetime.now()
        return cls.objects(id=attr.pop('id')).update(**attr)

    def to_temp_html(self):
        print('INFO: URL: ', self.url)
        FileUtils.to_html_file(path=FileUtils.conf.DIST_PATH + '/tmp.html', data=self.get_html())
        return True

    @classmethod
    def crud_get(cls, id, by='id'):
        ''' id, url, name'''
        try:
            if by == 'id':
                return cls.objects.get(id=id)

            return cls.objects.get(**{by: id})
        except Exception as e:
            print('ERROR: ', e)
        return None

    @classmethod
    def crud_create(cls, attr):
        return cls(**attr).save()

    @classmethod
    def file_to_db(cls, path, file_name_only=False):
        for file in FileUtils.get_all_files_recursive(path, endswith=None, file_name_only=file_name_only):
            # cls.save_url(file, attr={'image': '\\ftops' + file, 'name': file})
            print('.', end='', flush=True)

    @classmethod
    def get_cls_meta(cls):
        c = FileUtils.conf._connection[cls._db_alias if cls._db_alias else 'default'] # host/db_name
        db = cls._db_alias.split('/')[-1] if cls._db_alias != 'default' else FileUtils.conf.DATABASE_NAME
        host = str(c).split("'")[1]
        return '%s/%s - %s - html_path: %s' % (host, db, cls.get_collection_name(), cls.get_html_path())

    @classmethod
    def create_index_cols(cls, keys, background=False, **kwargs):
        cls.create_index(keys, background=background, **kwargs)

if __name__ == '__main__':

    # wiki = BaseDocument.get_class('WikiPage', db_name='ml', other_db=True)
    wiki = BaseDocument.get_class('test', db_name='sale')
    print(wiki.get_all_tables())
    # print(wiki.save_url('test1'))
    # wiki.new_field = StringField()

    # obj = wiki.save_url('test2', attr={'name': '2', 'has_html_1': False}, update_modified_date=True)

    # print(wiki.get_cls_meta())

    # # seed Data
    # wiki.save_url('test3', attr={'name': '3', 'has_html_1': True}, update_modified_date=True)
    # wiki.save_url('test4', attr={'name': '4'}, update_modified_date=True)
    # wiki.save_url('test5', data={'name': '5', 'has_html_1': True}, update_modified_date=True)
    # wiki.save_url('test6', name='5', update_modified_date=True)
    #
    # print(wiki.get_schema())
    # print(wiki.crud_get('2', 'name').get_json())

    # item = wiki.get_one_item()
    # print(item.save_log())
    # # print(item.save_log())
    # print(item.save_log())
    # print(item.save_log())
    # print(item.save_log())

    # qs = wiki.get_one(-1, offset=10)
    # for item in wiki.get_one(-1, offset=10, order_by=['-id']):
    #     print(item)

    # pprint(BaseDocument.get_class('note_log').get_one(where_id='5eef8cd12bf993a004993049'))

    # file_h = BaseDocument.get_class('file_ftops')
    # pprint(file_h.file_to_db('G:/z-wall/ftops', file_name_only=True))

    # for item in wiki.get_one(1):
    #     print(type(getattr(item, 'id').toString()))
    # print(FileUtils.conf)

    # wiki.zip_data_to_desktop()

    # for item in wiki.get_one(-1):
    #     print(item.get_created_at())

    # page = wiki()
    # page.data = {'test': 4, 'ds': 2}
    # page.name = '3333'
    # page.url = 'willnguyen.work'
    # page.save()

    # wiki.delete_html(lst=['5dcbfb827742180574512298', '5dcc2a48882d4c7180ca1137'])
    # item = wiki.get_by_url('willnguyen.work5')
    # print(wiki.get_ids())

    # for item in wiki.get_one(-1):
    #     print('record', item)

    # obj = wiki.save_url('willnguyen.work7')
    # print(obj.get_html())

    # print(WikiPage.insert_record({'url': 'fdfd', 'name': 'dd', 'data': {"33":3}}))
