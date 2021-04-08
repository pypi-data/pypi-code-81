import subprocess
import hashlib
import tempfile
import shutil
import sys
import re
import os
from contextlib import contextmanager
from sys import version_info


# Errors for Abstract Classes

class DirectAbstractMethodCallError(Exception):
    def __init__(self, msg=""):
        self.msg = (
            "DirectAbtractMethodCallError:\n"
            " You attemted to call a abstract method of an abstract class.\n"
            " Most likeley you want to use a conrete implementation of the class.\n"
            "\n"
            " If you want to write your own you need to follow the following steps\n"
            " First, you need to create a subclass of the abstract class\n"
            " that inherits from it, then you need to implement the function.\n"
            " After instantiating the new class you can freely use the function"
            "\n{msg}\n").format(msg=msg) 
        super().__init__(self.msg)

class NotImplementedError(Exception):
    def __init__(self, msg=""):
        self.msg = (
               "{msg}\nSorry this feature is not implemented as of yet!!\n"
               "If you are a dev, this is a call to action."
               "Seeing this message means that this"
               " part of the code is needed and requires attention!"
               "".format(msg=msg))
        super().__init__(self.msg)

class ToolInfoNotFoundError(Exception):
    def __init__(self, msg, ToolInfo):
        self.msg = (msg + 
                "\n > {call}: was not found in path\n "
                "and is also unreachable from the current working"
                "directory".format(call=ToolInfo.call)) 
        super().__init__(self.msg)

class ToolInfo():
    version_parser = lambda x: x
    def __init__(self, call,  version_call=[], version_parser=lambda x: x):
        self.call = call
        self.version_call = version_call
        self.version_parser = lambda x: x
        self.tool_found=False
        self.version_set=False
        self.path = None
        self.version= None
        self.get_tool_path() 
        self.get_version()
    
    def get_tool_path(self):
        self.tool_found = False
        try:
            response = mod_string(
                    subprocess.check_output(["which", self.call])).strip()
            self.path = response
            self.tool_found = True
        except:
            raise ToolInfoNotFoundError("Could not find Tool", self)


    def get_version(self):
        self.version_set=False
        if not self.version_call:
            self.version = "UNKNOWN"
        else:
            try:
                response = mod_string(
                        subprocess.check_output(self.version_call)).strip()
                self.version = response
                self.version_set = True
            except Exception as e:
                self.version = "NO_VERSION_FOUND"
                raise ToolInfoNotFoundError(
                        "Could not get version from version call:\n"
                        " {msg}\n\n"
                        " {_except}"
                        "".format(msg=" ".join(self.version_call),
                                  _except=type(e)), self)
        
class ErrorRealpathifyNeedsCallable(Exception):
    """Exception
    
    Realpathify bakes this exception into realpathified non-functions.
    This happens when the function used is not a callable or function. 

    Args: 

        msg (:obj:`str`): (optional) defaults to empty string
    
    Attributes:

        msg (:obj:`str`): Msg optionally augmented by msg given in class
            constructor
    """
    def __init__(self, msg=""):
        self.msg = ("ERROR in use of realpathify function!\n"
                    "it needs to be applied to a callable function like object."
                    "\n {msg}.").format(msg=msg)
        super().__init__(self.msg)


def eprint(*args, **kwargs):
    '''
    print function that prints to stderr

    :return: returns nothing
    '''
    print(*args, file=sys.stderr, **kwargs)


def mod_string(string):
    if (version_info > (3, 0)):
        return string.decode()
    else:
        return string


def check_if_file(_file):
    if not os.path.isfile(_file):
        raise ValueError("{_file} cannot be found".format(_file=_file))
    return _file

def check_if_directory(_dir):
    if not os.path.isdir(_dir):
        raise ValueError("{_dir} not a reachable directory".format(_dir=_dir))
    return _dir

def check_if_file_or_directory(_file_dir):
    if not os.path.isfile(_file_dir) and not os.path.isdir(_file_dir):
        raise ValueError("{_file_dir} cannot be found".format(_file_dir=_file_dir))
    return _file_dir


def validate_tsv_ext(_file, check_exists=True):
    """ Utility function that checks if tsv has correct extension

    Also checks if file exists
    """
    if not re.match(r'.*(.tab$|.tsv$)', _file):
        raise ValueError("{_file}: does not have a "
                         "standard fasta extension".format(_file=_file))
    if check_exists and not os.path.isfile(_file):
        raise ValueError("{_file}: does not exist".format(_file=_file))
    return _file

def validate_fasta_ext(_file, check_exists=True):
    """ Utility function that checks if fasta has correct extension

    Also checks if file exists
    """
    if not re.match(r'.*(.fa$|.fasta$|.fna$|.fn$)', _file):
        raise ValueError("{_file}: does not have a "
                         "standard fasta extension".format(_file=_file))
    if check_exists and not os.path.isfile(_file):
        raise ValueError("{_file}: does not exist".format(_file=_file))
    return _file

def validate_gff_ext(_file, check_exists=True):
    """ Utility function that checks if fasta has correct extension

    Also checks if file exists

    Args: 

        _file (:obj:`str`): file to check the extension off
        check_exists (optional :obj:`bool`): Default is True resulting in an
            existance check being performed
    """
    if not re.match(".*.gff$", _file):
        raise ValueError("{_file}: does not have a "
                         "standard gff extension".format(_file=_file))
    if check_exists and not os.path.isfile(_file):
        raise ValueError("{_file}: does not exist".format(_file=_file))
    return _file

def realpathify(func):
    """function that modifies other function to return realpath

    needs a function method (a bit of functional programming)

    Args:
        func ( object with _call_ attribute ): Some function or otherwise
            callable object whose return will be modified
            
    Returns:
        callable or function whose return is modified with a os.path.realpath
        call. That function raises :class:`ErrorRealpathifyNeedsCallable` if
        it is no function. 
    """
    def realpathed_fun(*args, **kwargs):
        try: 
            return os.path.realpath(func(*args, **kwargs))
        except TypeError as e:
            raise ErrorRealpathifyNeedsCallable(str(e))


    return realpathed_fun


@contextmanager
def tmpdir():
    '''
    Generator/contextmanager that creates a temporary directory
    and removes the same directory after context exit

    Yields:
        temporary directory as :obj:`str`
    '''
    dirname = tempfile.mkdtemp()
    try:
        yield dirname
    finally:
        shutil.rmtree(dirname)


@contextmanager
def fifo():
    '''
    Generator/contextmanager that manages creation of a fifo
    '''
    dirname = tempfile.mkdtemp()
    try:
        path = os.path.join(dirname, 'tmp_fifo')
        os.mkfifo(path)
        yield path
    finally:
        shutil.rmtree(dirname)


@contextmanager
def pseudo_stderr():
    '''
    pseudo stdout context
    '''
    try:
        yield sys.stderr.buffer
    finally:
        pass



def hashfile(_file, BLOCK_SIZE = 65536):
        """generate a Hash for a file

        straight copy and paste from
        https://nitratine.net/blog/post/how-to-hash-files-in-python/ (2020)
	"""
        # The size of each read from the file
        file_hash = hashlib.sha256()
        with open(_file, 'rb') as f:
            fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
            while len(fb) > 0: # While there is still data being read from the file
                file_hash.update(fb) # Update the hash
                fb = f.read(BLOCK_SIZE)
        return file_hash.hexdigest()


def hashstring(string):
    string_hash = hashlib.sha256()
    string_hash.update(string.encode())
    return string_hash.hexdigest()


def strip_empty_lines(string_lines):
    """removes empty lines from list of lines"""
    return list(filter(lambda x: not re.match(r'^\s*$', x), string_lines))



def default_if_not(key, _dict, default):
    try:
        return _dict[key]
    except KeyError:
        return default

def mkdir_if_not_exists(_dir):
    """ Make directory if it does not exist
    
    python 3.2 added the used exist_ok flag #PY3.2<
    """
    if _dir is None:
        return None
    try:
        os.makedirs(_dir, exist_ok=True)
        return os.path.realpath(_dir)
    except Exception as e:
        eprint(e)
        raise  
    

def walklevel(some_dir, level=1):
    """ os walk with recursion limit

    Thanks to Stackoverflow User nosklo
    https://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
    """
    if level==0:
        yield os.walk(some_dir)
        return
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir, topdown=True):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def cleanup_file_for_hashing(regex, file, outfile_name):
    with open(outfile_name, 'wb') as outfile:
        with subprocess.Popen(['perl', '-pe', regex, file],
                              stdout=outfile) as clean_proc:
            clean_proc.wait()
            if clean_proc.returncode:
                raise subprocess.CalledProcessError(
                        clean_proc.returncode,
                        "Perl Regex failed")
