import markdown
import os
import json
import errno
from glob import glob

def cli():
    def compile():
        if os.path.isfile('convert.json'):
            with open('convert.json', 'r') as j:
                data = json.load(j)
                filename = data['name']
                if os.path.isfile(filename):
                    with open(filename, 'r') as md:
                        text = md.read()
                        html = markdown.markdown(text)
                    hfile = filename.replace('.md', '.html')
                    with open(f'{hfile}', 'w') as fh:
                        fh.write(html)
                else:
                    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), 'convert.json')
    def init():
        if os.path.isfile('convert.json'):
            return "File Existed!"
        else:
            dir = os.getcwd()
            chdir(dir)
            files = glob('*.'+'md')
            for file in files:
                file = file[0]
                data = {
                    "name": str(file)
                }
                with open('convert.json', 'w') as convert:
                    json.dump(data, convert)
    init = init()
    compile = compile()