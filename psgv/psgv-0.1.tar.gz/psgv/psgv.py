import os
import json

class psgv(object):
    """ Sets arbitrary variables types as an environment variable in Unix

    """
    def __init__(self, key=None):
        self._val = None
        self._key = key


    @property
    def key(self):
        """ The environment variable key
        """
        if self._key is not None:
            return self._key
        else:
            return False

    @key.setter
    def key(self, key):
        self._key = key

    @key.deleter
    def key(self):
        del self._key

    @property
    def val(self):
        """I'm the 'x' property."""
        if (self._key is not None) and \
                (os.path.isfile(os.path.join('/var/tmp/', self._key))):
            with open('/var/tmp/' + self._key, 'r') as f:
                value = json.load(f)
            if isinstance(value, dict):
                value = envdict(value)
                value.parent = self
            if isinstance(value, list):
                value = envlist(value)
                value.parent = self
            return value
        else:
            return False

    @val.setter
    def val(self, value):
        if isinstance(value, dict):
            value = envdict(value)
            value.parent = self
            self._val = value
        if isinstance(value, bool):
            self._val = value
        if isinstance(value, list):
            value = envlist(value)
            value.parent = self
            self._val = value
        else:
            self._val = value
        if self._key is not None:
            with open('/var/tmp/' + self._key, 'w') as f:
                json.dump(self._val, f)
        else:
            return None

    @val.deleter
    def val(self):
        del self._val

class envdict(dict):
    def __init__(self, *args, **kwargs):
        super(envdict, self).update(*args, **kwargs)
        self.parent = None

    def __getitem__(self, key):
        val = super(envdict, self).__getitem__(key)
        return val

    def __setitem__(self, key, val):
        _dict = dict(self.parent.val)
        _dict[key] = val
        super(envdict, self).update(_dict)
        self.parent.val = self

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v

class envlist(list):
    def __init__(self, *args):
        super(envlist, self).__init__(*args)
        self.parent = None

    def __getitem__(self, key):
        val = super(envlist, self).__getitem__(key)
        return val

    def __setitem__(self, key, val):
        _list = list(self.parent.val)
        super(envlist, self).__setitem__(key, val)
        self.parent.val = self

    def __add__(self, val):
        _list = list(self.parent.val)
        if isinstance(val, list):
            theval = val
        else:
            theval = [val]
        _list = super(envlist, self).__add__(theval)
        super(envlist, self).__init__(_list)
        self.parent.val = self
        return self

    def extend(self, *args):
        _list = list(self.parent.val)
        for arg in args:
            for val in arg:
                self.__add__(val)

"""
import sys, token, tokenize

class MissingLabelError(Exception):
    'goto' without matching 'label'.
    pass

# Source filenames -> line numbers of plain gotos -> target label names.
_plainGotoCache = {}

# Source filenames -> line numbers of computed gotos -> identifier names.
_computedGotoCache = {}

# Source filenames -> line numbers of labels -> label names.
_labelCache = {}

# Source filenames -> label names -> line numbers of those labels.
_labelNameCache = {}

# Source filenames -> comefrom label names -> line numbers of those comefroms.
_comefromNameCache = {}

def _addToCaches(moduleFilename):
    Finds the labels and gotos in a module and adds them to the caches.

    # The token patterns that denote gotos and labels.
    plainGotoPattern = [(token.NAME, 'goto'), (token.OP, '.')]
    computedGotoPattern = [(token.NAME, 'goto'), (token.OP, '*')]
    labelPattern = [(token.NAME, 'label'), (token.OP, '.')]
    comefromPattern = [(token.NAME, 'comefrom'), (token.OP, '.')]

    # Initialise this module's cache entries.
    _plainGotoCache[moduleFilename] = {}
    _computedGotoCache[moduleFilename] = {}
    _labelCache[moduleFilename] = {}
    _labelNameCache[moduleFilename] = {}
    _comefromNameCache[moduleFilename] = {}

    # Tokenize the module; 'window' is the last two (type, string) pairs.
    window = [(None, ''), (None, '')]
    for tokenType, tokenString, (startRow, startCol), (endRow, endCol), line \
            in tokenize.generate_tokens(open(moduleFilename, 'r').readline):
        # Plain goto: "goto .x"
        if window == plainGotoPattern:
            _plainGotoCache[moduleFilename][startRow] = tokenString

        # Computed goto: "goto *identifier"  XXX Allow expressions.
        elif window == computedGotoPattern:
            _computedGotoCache[moduleFilename][startRow] = tokenString

        # Comefrom: "comefrom .x"  XXX Non-determinism via multiple comefroms.
        if window == comefromPattern:
            _comefromNameCache[moduleFilename][tokenString] = startRow

        # Label: "label .x"  XXX Computed labels.
        elif window == labelPattern:
            _labelCache[moduleFilename][startRow] = tokenString
            _labelNameCache[moduleFilename][tokenString] = startRow

        # Move the token window back by one.
        window = [window[1], (tokenType, tokenString)]

def _trace(frame, event, arg):
    # If this is the first time we've seen this source file, cache it.
    filename = frame.f_code.co_filename
    if filename not in _plainGotoCache:
        _addToCaches(filename)

    # Is there a goto on this line?
    targetLabel = _plainGotoCache[filename].get(frame.f_lineno)
    if not targetLabel:
        # No plain goto.  Is there a computed goto?
        identifier = _computedGotoCache[filename].get(frame.f_lineno)
        if identifier:
            # If eval explodes, just let the exception propagate.
            targetLabel = eval(identifier, frame.f_globals, frame.f_locals)

    # Jump to the label's line.
    if targetLabel:
        try:
            targetLine = _labelNameCache[filename][targetLabel]
        except KeyError:
            raise MissingLabelError, "Missing label: %s" % targetLabel
        frame.f_lineno = targetLine

    # Is there a label on this line with a corresponding comefrom?
    label = _labelCache[filename].get(frame.f_lineno)
    if label:
        targetComefromLine = _comefromNameCache[filename].get(label)
        if targetComefromLine:
            frame.f_lineno = targetComefromLine

    return _trace

# Install the trace function, including all preceding frames.
sys.settrace(_trace)
frame = sys._getframe().f_back
while frame:
    frame.f_trace = _trace
    frame = frame.f_back

# Define the so-called keywords for importing: 'goto', 'label' and 'comefrom'.
class _Label:
    Allows arbitrary x.y attribute lookups.
    def __getattr__(self, name):
        return None

goto = None
label = _Label()
comefrom = _Label()
"""
