from os import name
import webbrowser
from pathlib import Path
from . import encrypt
from .file_server import flask_server
import hashlib
import os
import click
# import shutil
ENCODE_CODE = [chr(i) for i in  range(ord('a'),ord('z')+1)] + [chr(i) for i in  range(ord('A'),ord('Z')+1)]
ENCODE_CODE += [chr(i) for i in  range(ord('0'),ord('9')+1)]
ENCODE_CODE = (''.join(ENCODE_CODE)).encode()
class yxsFile:
    XS_SUFFIX = set(('.xsd','.xsf','.mpxs','.jpxs'))
    def __init__(self,filename,workdir=None,passwd=None):
        if passwd is None:
            passwd = encrypt.get_default_passwd()
        self.filename = Path(filename)
        self.title_size = 2048
        self.passwd = passwd
        self.file_suffix = '.mpxs','.jpxs'
        if self.filename.suffix in self.file_suffix:
            self.is_pureFile = False
        else:
            self.is_pureFile = True
        self.workdir = workdir 
        if workdir is None:
            self.workdir = self.filename.parent
    def to_pureFile(self,to_dir = None):
        if not self.is_pureFile:
            fp   = open(self.filename,'rb')
            title = fp.read(self.title_size).replace(bytes([0]),b'')
            new_name = self.filename.parent/title.decode()
            if to_dir:
                new_name = Path(to_dir)/new_name.name
            while new_name.exists():
                new_name = new_name.parent/('new_'+new_name.name)
            fpp = open(new_name,'wb')
            t = fp.read(1024*1024*8)
            while t != b'':
                fpp.write(t)
                t = fp.read(1024*1024*32)
        else: 
            new_name = None 
        return new_name

    def to_yxsFile(self,to_dir=None):
        if self.is_pureFile:
            name = self.filename.name.encode()
            yxs_filenme = self.encode_filename()
            newname_stem = self.filename.stem
            ii = 1
            while yxs_filenme.is_file():
                newname = self.filename.parent / (newname_stem+f'_{ii}{self.filename.suffix}')
                yxs_filenme = self.encode_filename(newname)
                ii += 1
            if to_dir:
                yxs_filenme = Path(to_dir)/yxs_filenme.name
            fpxs = open(yxs_filenme,'wb')
            fp   = open(self.filename,'rb')
            tbytes = bytes([0]*(self.title_size-len(name)))
            t = name+tbytes
            while t != b'':
                fpxs.write(t)
                t = fp.read(1024*1024*32)
        else:
            yxs_filenme = None 
        return yxs_filenme

    def play_video(self):
        webbrowser.open('http://0.0.0.0:9090/'+self.filename.name+'?player=default')
        os.chdir(self.filename.parent)
        flask_server.main(9090)
    def view_image(self):
        pass
    def encode_filename(self,filename=None):
        if not filename:
            filename = self.filename
        else:
            filename = Path(filename)
        name = filename.name
        suffix = filename.suffix 
        if suffix in self.XS_SUFFIX:
            return filename
        if filename.is_dir():
            mysuffix = '.xsd'
        else:
            mysuffix = '.xsf'
        if suffix == '.jpg':
            mysuffix = '.jpxs'
            name = filename.stem
        if suffix == '.mp4':
            mysuffix = '.mpxs'
            name = filename.stem
        length= len(name)
        while True:
            spname = encrypt.spencode(name[:length].encode(),self.passwd,str_set=ENCODE_CODE).decode()
            if len(spname)< 250:
                break 
            else:
                length = int(length / 2)
        spname = spname + mysuffix 
        return filename.parent/ spname
    def decode_filename(self):
        suffix = self.filename.suffix 
        if suffix in self.XS_SUFFIX:
            stem = self.filename.stem
            try:
                spname = encrypt.spdecode(stem.encode(),self.passwd,str_set=ENCODE_CODE).decode()
            except:
                print(stem)
                exit()
            if suffix == '.mpxs':
                mysuffix = '.mp4'
            elif suffix == '.jpxs':
                mysuffix = '.jpg'
            else: 
                mysuffix = ''

            return self.filename.parent / (spname+mysuffix)
        else:
            return self.filename

    def get_md5(self):
        fp = open(self.filename,'rb')
        if not self.is_pureFile:
            fp.read(self.title_size)
        md5 = hashlib.md5()
        while True:
            t = fp.read(1024*1024*4)
            if t == b'':
                break
            md5.update(t)
        return md5
def listdir(dirname):
    result = []
    for i in os.listdir(dirname):
        t = str(yxsFile(i).decode_filename())
        result.append((t,len(t),i))
    result.sort(key = lambda x:x[0])
    max_length = max([i[1] for i in result])
    f = '{:'+str(max_length+2)+'s}-> {}'
    for dname,_,ename in result:

        if dname != ename:
            print(f.format(dname,ename))
        else:
            print(dname)

def find_file(find_str):
    find_str = find_str.lower()
    fmt = '{} -> {}'
    for root,ds,fs in os.walk('./'):
        rootp = Path(root)
        for i in fs:
            rp = rootp / i 
            if not rp.is_symlink():
                t = str(yxsFile(i).decode_filename())
                if t.lower().find(find_str) != -1:
                    tname = rootp / t
                    iname = rootp / i
                    if t != i:
                        print(fmt.format(tname,iname))
                    else:
                        print(iname)

@click.command()
@click.argument('args',nargs=-1)
@click.option('--filename','-i',default=None,help="输入文件名或者文件夹名称")
@click.option('--pure','-p',default=False,is_flag=True,help="转化为原始文件")
@click.option('--xfile','-x',default=False,is_flag=True,help="加密该文件")
@click.option('--find','-f',default='',help="查找文件")
@click.option('--decode','-d',default=False,is_flag=True,help="单独显示原文件名,不转码文件,文件名后缀改为._tt")
@click.option('--encode','-e',default=False,is_flag=True,help="加密显示文件名(._tt)")
def main(args=None,filename=None,pure=False,xfile=False,find=None,decode=False,encode=False):
    key_option = 0
    if find:
        key_option += 1
        find_file(find)
    if decode:
        key_option += 1
        for i in os.listdir('./'):
            if not i.endswith('._tt'):
                df = yxsFile(i).decode_filename().name
                if df != i:
                    suffix = Path(i).suffix
                    os.rename(i,df+suffix+'._tt')
    if encode:
        key_option += 1
        for i in os.listdir('./'):
            if i.endswith('._tt'):
                istem = i[:-4]
                suffix = Path(istem).suffix
                ef = yxsFile(istem[:-len(suffix)]).encode_filename().name
                os.rename(i,Path(ef).with_suffix(suffix))
    
    filename_list = list()
    if key_option == 0:
        if filename:
            filename_list = [filename,]
        if args:
            filename_list.extend(args)
        if not filename and not args:
            listdir('./')
    for filename in filename_list:
        if pure:
            pf = yxsFile(filename)
            pf.to_pureFile()
            print(pf.decode_filename())
        elif xfile:
            pf = yxsFile(filename)
            pf.to_yxsFile()
            print(filename,'->',pf.decode_filename())
        else:
            pf = yxsFile(filename)
            suffix = Path(filename).suffix
            if suffix == '.mpxs':
                pf.play_video()
if __name__=='__main__':
    main()
