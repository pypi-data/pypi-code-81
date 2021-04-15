"""Customized attributes
"""

import re
import os
import shutil
import json
from numbers import Number, Integral

import numpy as np
import datajoint as dj

from loris.database.attribute_mixin import Placeholder, ProcessMixin
from loris.errors import LorisSerializationError
from loris.io import spickledumps, spickleloads


class TrueBool(dj.AttributeAdapter):

    attribute_type = 'bool'

    def put(self, obj):
        if obj is None or np.isnan(obj):
            return
        return bool(obj)

    def get(self, value):
        return bool(value)


class SavePickleMixin:

    def put(self, obj):
        if obj is None:
            return
        return spickledumps(obj)

    def get(self, value):
        return spickleloads(value)


class PickleBlob(SavePickleMixin, dj.AttributeAdapter):

    attribute_type = 'longblob'


class PickleData(SavePickleMixin, dj.AttributeAdapter):

    attribute_type = 'blob@datastore'


class ArrMixin:

    def __init__(self, ndim=None, shape=None, atleast=False):
        self.ndim = ndim
        self.shape = shape
        self.atleast = atleast

    def put(self, obj):
        if obj is None:
            return

        if not isinstance(obj, np.ndarray):
            raise TypeError(f"object must be of type `numpy.ndarray`, but is of type `{type(obj)}`")

        if self.ndim is None and self.shape is None:
            return obj

        if self.ndim is not None:
            if self.atleast:
                assert obj.ndim >= self.ndim, f"object has dimensionality `{obj.ndim}`, but only dimensionality `{self.ndim}` or above is allowed."
            else:
                assert obj.ndim == self.ndim, f"object has dimensionality `{obj.ndim}`, but only dimensionality `{self.ndim}` is allowed."

        if self.shape is not None:
            for dim, (allowed_len, is_len) in enumerate(zip(self.shape[::-1], obj.shape[::-1])):
                assert allowed_len == is_len, f"object has length `{is_len}` for dimension {dim}, but must be length `{allowed_len}`"

        return obj

    def get(self, obj):
        return obj


class ArrStore(ArrMixin, dj.AttributeAdapter):
    attribute_type = 'blob@datastore'


class ArrBlob(ArrMixin, dj.AttributeAdapter):
    attribute_type = 'longblob'


class LookupName(dj.AttributeAdapter):
    """a string with stripped of
    """

    attribute_type = 'varchar(127)'

    def put(self, obj):
        if obj is None:
            return

        if isinstance(obj, str):
            obj = obj.strip()  # .lower() - removed since MySQL does not distinguish
        else:
            raise dj.DataJointError(
                f"lookup name '{obj}' must be of type "
                f"'str' and not '{type(obj)}'."
            )

        if not obj.isidentifier():
            raise dj.DataJointError(
                f"lookup name '{obj}' is not an identifier; "
                "it containes characters besides alphanumeric and/or "
                "an underscore."
            )

        return obj

    def get(self, value):
        return value


class PrefixId(dj.AttributeAdapter):
    """
    Prefix id
    """

    attribute_type = 'varchar(127)'

    def __init__(self, prefix=''):
        super().__init__()
        self.prefix = prefix

    def put(self, obj):
        if obj is None:
            return

        if isinstance(obj, str):
            if obj.startswith(self.prefix):
                obj = obj[len(self.prefix):]
            if obj.isnumeric():
                obj = int(obj)
            else:
                raise dj.DataJointError(
                    "Prefix Id must be an integer, but string is `{obj}`."
                )
        elif isinstance(obj, Integral):
            pass
        else:
            raise dj.DataJointError(
                f"Prefix Id must be an integer; but is of type `{type(obj)}`."
            )

        return f"{self.prefix}{obj}"

    def get(self, value):
        return value


class ListString(dj.AttributeAdapter):

    attribute_type = 'varchar(4000)'

    def __init__(self, ele_truth_call=None, error_message=None):
        self.ele_truth_call = ele_truth_call
        self.error_message = error_message

    def put(self, obj):
        if obj is None:
            return
        if isinstance(obj, str):
            try:
                obj = json.loads(obj)
            except Exception as e:
                raise LorisSerializationError(
                    f'Data is not a json-serializable: {e}'
                )
        assert isinstance(obj, (list, tuple)), \
            f'object must be list or tuple for liststring type: {type(obj)}'
        if self.ele_truth_call is not None:
            assert all([self.ele_truth_call(ele) for ele in obj]), \
                (
                    f'Not all object elements pass truth call.'
                    if self.error_message is None else self.error_message
                )
        return json.dumps(obj)

    def get(self, value):
        return json.loads(value)


class DictString(dj.AttributeAdapter):

    attribute_type = 'varchar(4000)'

    def __init__(self, val_truth_call=None, error_message=None):
        self.val_truth_call = val_truth_call
        self.error_message = error_message

    def put(self, obj):
        if obj is None:
            return
        if isinstance(obj, str):
            try:
                obj = json.loads(obj)
            except Exception as e:
                raise LorisSerializationError(
                    f'Data is not a json-serializable: {e}'
                )
        assert isinstance(obj, (dict)), \
            f'object must be dict for dictstring type: {type(obj)}'
        if self.val_truth_call is not None:
            assert all([self.val_truth_call(val) for val in obj.values()]), \
                (
                    f'Not all object values pass truth call.'
                    if self.error_message is None else self.error_message
                )
        return json.dumps(obj)

    def get(self, value):
        return json.loads(value)


class Chromosome(dj.AttributeAdapter):

    attribute_type = 'varchar(511)'

    def put(self, obj):
        """perform checks before putting
        """

        if obj is None:
            return

        assert isinstance(obj, str), (
            f"object is not of type string, "
            f"but {type(obj)} for chromosome attribute")

        obj = obj.strip()

        return obj

    def get(self, value):
        return value


class Email(dj.AttributeAdapter):

    attribute_type = 'varchar(255)'

    @staticmethod
    def is_email(obj):

        regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        return re.fullmatch(regex, obj) is not None

    def put(self, obj):
        """perform checks before putting
        """

        if obj is None:
            return

        assert isinstance(obj, str), (
            f"object is not of type string, "
            f"but {type(obj)} for email attribute")

        obj = obj.strip()

        if not self.is_email(obj):
            raise dj.DatajointError(
                f"string {obj} is not a valid email for attribute {self}"
            )

        return obj

    def get(self, value):
        return value


class Link(dj.AttributeAdapter):

    attribute_type = 'varchar(511)'

    @staticmethod
    def is_url(obj):

        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )

        return re.fullmatch(regex, obj) is not None

    def put(self, obj):
        """perform checks before putting
        """

        if obj is None:
            return

        assert isinstance(obj, str), (
            f"object is not of type string, "
            f"but {type(obj)} for link attribute")

        obj = obj.strip()

        if not self.is_url(obj):
            raise dj.DatajointError(
                f"string {obj} is not a url for attribute {self}"
            )

        return obj

    def get(self, value):
        return value


class FlyIdentifier(dj.AttributeAdapter):

    attribute_type = 'varchar(255)'

    def put(self, obj):
        """perform checks before putting
        """

        if obj is None:
            return

        assert isinstance(obj, str), (
            f"object is not of type string, "
            f"but {type(obj)} for fly identifier attribute")

        obj = obj.strip()

        return obj

    def get(self, value):
        return value


class Phone(dj.AttributeAdapter):

    attribute_type = 'varchar(16)'

    def put(self, obj):
        """perform checks before putting
        """

        if obj is None:
            return

        assert isinstance(obj, str), (
            f"object is not of type string, "
            f"but {type(obj)} for phone attribute")

        obj = obj.strip()

        return obj

    def get(self, value):
        return value


class CrossSchema(dj.AttributeAdapter):

    attribute_type = 'attach@attachstore'

    def put(self, obj):
        """perform checks before putting
        """

        if obj is None:
            return

        return obj

    def get(self, value):
        return value


class TarFolder(dj.AttributeAdapter):

    attribute_type = 'attach@attachstore'

    def put(self, obj):
        """perform checks before putting and archive folder
        """

        if obj is None:
            return

        assert os.path.exists(obj), f'path {obj} does not exist.'

        return shutil.make_archive(obj, 'tar', obj)

    def get(self, value):
        """unpack zip file
        """
        unpacked_file = os.path.splitext(value)[0]
        shutil.unpack_archive(value, unpacked_file)
        return unpacked_file


class AttachProcess(dj.AttributeAdapter, ProcessMixin):

    attribute_type = 'attach@attachstore'

    def put(self, obj):
        return self.put_process(obj)

    def get(self, value):
        return self.get_process(value)


class AttachPlaceholder(dj.AttributeAdapter, ProcessMixin):

    attribute_type = 'attach@attachstore'

    def put(self, obj):
        """perform checks before putting and archive folder
        """

        if obj is None:
            return

        obj = self.put_process(obj)
        return Placeholder(obj).write()

    def get(self, value):
        """get file
        """
        return self.get_process(Placeholder.read(value))


class FolderPath(dj.AttributeAdapter):

    attribute_type = 'varchar(511)'

    def put(self, obj):

        if obj is None:
            return
        elif not isinstance(obj, str):
            raise TypeError(
                f"Object must be string type, but is {type(obj)}"
            )

        if not os.path.exists(obj):
            raise ValueError(
                f"Path `{obj}` does not exist."
            )

        if not os.path.isdir(obj):
            raise ValueError(
                f"Path `{obj}` is not a directory."
            )

        return obj

    def get(self, value):
        return value


class DreyeJSON(dj.AttributeAdapter):
    """
    Use dreye (de)serializer
    """

    attribute_type = 'blob@datastore'

    def put(self, obj):

        if obj is None:
            return

        from dreye.io.serialization import dump_json
        return dump_json(obj)

    def get(self, value):
        from dreye.io.serialization import load_json
        return load_json(value)


chr = Chromosome()
link = Link()
flyidentifier = FlyIdentifier()
crossschema = CrossSchema()
truebool = TrueBool()
tarfolder = TarFolder()
liststring = ListString()
dreyejson = DreyeJSON()
tags = ListString(
    lambda x: isinstance(x, str),
    'Elements of list must be strings.'
)
numberlist = ListString(
    lambda x: isinstance(x, Number),
    'Elements of list must be strings.'
)
listintervals = ListString(
    lambda x: (
        (isinstance(x, (list, tuple)))
        and (len(x) == 2)
        and (isinstance(x[0], Number))
        and (isinstance(x[1], Number))
    ),
    'Elements of list must be two-tuple of numbers (integers or float).'
)
dictstring = DictString()
dicttags = DictString(
    lambda x: isinstance(x, str),
    'Values of dict must be strings'
)
numberdict = DictString(
    lambda x: isinstance(x, Number),
    'Values of dict must be strings'
)
attachprocess = AttachProcess()
attachplaceholder = AttachPlaceholder()
lookupname = LookupName()
email = Email()
phone = Phone()
pickledata = PickleData()
pickleblob = PickleBlob()
folderpath = FolderPath()
stockid = PrefixId(prefix='s')

arrblob = ArrBlob()
arrstore = ArrStore()

arr1blob = ArrBlob(1)
arr1store = ArrStore(1)

arr2blob = ArrBlob(2)
arr2store = ArrStore(2)

arr3blob = ArrBlob(3)
arr3store = ArrStore(3)


custom_attributes_dict = {
    'chr': chr,
    'link': link,
    'flyidentifier': flyidentifier,
    'crossschema': crossschema,
    'truebool': truebool,
    'tarfolder': tarfolder,
    'liststring': liststring,
    'dictstring': dictstring,
    'dicttags': dicttags,
    'tags': tags,
    'attachprocess': attachprocess,
    'attachplaceholder': attachplaceholder,
    'lookupname': lookupname,
    'email': email,
    'phone': phone,
    'listintervals': listintervals,
    'pickledata': pickledata,
    'pickleblob': pickleblob,
    'folderpath': folderpath,
    'stockid': stockid,
    'dreyejson': dreyejson,
    'numberlist': numberlist,
    'numberdict': numberdict,
    'arrblob': arrblob,
    'arrstore': arrstore,
    'arr1blob': arr1blob,
    'arr1store': arr1store,
    'arr2blob': arr2blob,
    'arr2store': arr2store,
    'arr3blob': arr3blob,
    'arr3store': arr3store,
}
