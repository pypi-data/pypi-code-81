"Set code files free from unwieldy documentation!"
__version__ = '0.0.1'
import sys
import pickle
import json
import argparse
import os
from pathlib import Path
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.lexers import Lexer, PygmentsLexer
from pygments.lexers.markup import RstLexer

def hash_fn(fn):
    '''Hash a function. Returns the qualified name of a function. However,
    in the future this might return a unique hash. Right now, whenever this
    function is updated, all of the previous docstrings have to be retyped.
    A companion function, ``to_new_hash``, might be created.'''
    return fn.__qualname__

### Status Modifiers ###################################################################

def set_status(status):
    "Sets the status file (doc_config)"
    try:
        with open('doc_config', 'wb') as f: get_docstrings = pickle.dump(status, f)
    except FileNotFoundError: pass

def get_status():
    "Gets the status file"
    try:
        with open('doc_config', 'rb') as f: return pickle.load(f)
    except FileNotFoundError: pass

def init_status(status):
    "Creates the status file if it does not exist"
    try:
        with open('doc_config', 'xb') as f: pickle.dump(status, f)
    except FileExistsError: pass

def del_status():
    "Deletes the status file if it exists"
    try: Path('doc_config').unlink()
    except FileNotFoundError: pass

def make_store():
    "Create a docstrings.json if it does not exist or is empty"
    p = Path('docstrings.json')
    if not p.exists() or not p.read_text():
        Path('docstrings.json').write_text('{}')

def _get_store():
    "Gets the entire contents of docstrings.json"
    with open('docstrings.json') as f: return json.load(f)

def add_store(fn, docstring):
    "Add a function to docstrings.json"
    d = {**_get_store(), hash_fn(fn): docstring}
    with open('docstrings.json', 'w') as f: json.dump(d, f)

def get_store(fn):
    "Get the docstring of a function from docstrings.json"
    return _get_store()[hash_fn(fn)]

### Askers #############################################################################

def confirm(s):
    '''Simple function to determine whether a string conveys assent or dissent.
    This function decides that a string conveys assent if its first character is a
    ``y``.'''
    return s and s.strip().lower()[0] == 'y'

class ConfirmationLexer(Lexer):
    "A lexer to highlight values meaning yes as green and values meaning no as red."
    def lex_document(document):
        return lambda x: [('#00ff00', document.text)] if confirm(document.text) else [('#ff0000', document.text)]

def ask_docstring(fn_name):
    "Ask for the docstring of a function given a function's name."
    print_formatted_text(HTML(f'Enter the docstring for <ansigreen>{fn_name}</ansigreen> (Press Escape then Enter to submit):'))
    return prompt('1| ', multiline=True, lexer=PygmentsLexer(RstLexer), prompt_continuation=lambda width, line_no, is_soft_wrap: f'{line_no + 1}| ')

def ask_confirmation(fn_name):
    "Ask for confirmation (used to determine whether an existing docstring should be overwritten)."
    return not confirm(prompt(f'Do you wish to overwrite the docstring for {fn_name}? [y/N] ', lexer=ConfirmationLexer))

### Documentors ########################################################################

def add_doc(fn):
    '''This function is the entire UI used to get the docstring of a single function.
    It first determines if the function has already been documented; if it already has a docstring
    or exists in ``docstrings.json``, a confirmation will be asked. If the user responds with ``yes``
    or the function isn't documented, it open up a multiline prompt with reST hightlighting for the
    user to type the documentation. Once they submit with Escape then Enter (or Meta+Enter), the docstring
    will be saved in ``docstrings.json``'''
    if (fn.__doc__ or str(hash_fn(fn)) in _get_store()) and ask_confirmation(fn.__qualname__):
        return
    add_store(fn, ask_docstring(fn.__qualname__))

def doc(fn):
    "Decorate functions you want to be documented with this decorator."
    if get_status():
        add_doc(fn)
    else:
        fn.__doc__ = get_store(fn)
    return fn

def poll(modules):
    "Prompt and save all the docstrings of the functions decorated with :func:`doc` in the modules provided."
    set_status(True)
    for x in modules:
        __import__(x)
    set_status(False)

def main():
    "Main function"
    sys.path.insert(0, os.getcwd())
    make_store()
    init_status(True)
    parser = argparse.ArgumentParser(description="Define docstrings in the modules passed as arguments.")
    parser.add_argument('module', nargs='+', help="A module to define docstrings in")
    args = parser.parse_args()
    poll(map(lambda x: '.'.join(x.split('.')[0:-1]), args.module))
    del_status()

if __name__ == '__main__':
    main()
