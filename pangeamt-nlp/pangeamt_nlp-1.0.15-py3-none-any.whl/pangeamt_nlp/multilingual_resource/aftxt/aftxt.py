from pangeamt_nlp.utils.raise_exception_if_file_not_found import raise_exception_if_file_not_found
from pangeamt_nlp.utils.raise_exception_if_file_found import raise_exception_if_file_found
from pangeamt_nlp.multilingual_resource.multilingual_resource_base import MultilingualResourceBase



class AfTxt(MultilingualResourceBase):
    SEP = '|||'

    def __init__(self, file):
        super().__init__(MultilingualResourceBase.TYPE_AFTXT)
        raise_exception_if_file_not_found(file)
        self._file = file
        self._num_trans_units = None
        self._num_words_units = None
        self._num_chars_units = None

    @staticmethod
    def new(file:str):
        raise_exception_if_file_found(file)
        return AfTxt(file)

    def read(self, reader=None):
        with open(self._file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = line.strip()
                parts = line.split(self.SEP)
                try:
                    left = parts[1]
                    right = parts[2]
                except:
                    raise ValueError("Invalid line {}".format(i+1))
                if reader:
                    yield reader.read(left, right)
                else:
                    yield left, right

    def get_file(self):
        return self._file
    file = property(get_file)

    def get_num_trans_units(self):
        if self._num_trans_units is None:
            num = 0
            with open(self._file, 'rb') as f:
                for line in f:
                    #line = line.decode('utf-8')
                    num += 1
            return num
        return self._num_trans_units
    num_trans_units = property(get_num_trans_units)

    def get_num_chars_units(self):
        if self._num_chars_units is None:
            num = 0
            with open(self._file, 'r', encoding='utf-8') as f:
                for line in f:
                    line_split = line.split(self.SEP)
                    num += len(line_split[1].strip()) + len(line_split[2].strip())
            return num
        return self._num_chars_units
    num_chars_units = property(get_num_chars_units)

    def get_num_words_units(self):
        if self._num_words_units is None:
            num = 0
            with open(self._file, 'r', encoding='utf-8') as f:
                for line in f:
                    line_split = line.split(self.SEP)
                    num += len(line_split[1].strip().split(' ')) + len(line_split[2].strip().split(' '))
            return num
        return self._num_words_units
    num_words_units = property(get_num_words_units)

    def get_writer(self):
        return self._writer
    writer = property(get_writer)

class AfTxtWriter:
    def __init__(self, file: str):
        self._file = file
        self._file_handler = None

    def __enter__(self):
        self._file_handler = open(self._file, 'a', encoding='utf-8')
        return self

    def __exit__(self, type, value, tb):
        self._file_handler.close()
        self._file_handler = None

    def write(self, id, left, right):
        self._file_handler.write(str(id) + AfTxt.SEP + left + AfTxt.SEP + right + '\n')

    def write_raw(self, line):
        self._file_handler.write(line)