import re
import sys

doc='''
   -NAMEOFTHING [TYPE] [default: DEFAULT]  [DOUBLESPACE DESCRIPTION]
--myintarg int default:12   blabla
--something    we will assume that it is a bool i think
--mystring str default:asd  blabla
'''

#REGEX:
#0:name
#1:type
#2: NOTHIG
#3:defaultvalue
getgroups = re.compile( '--([\w]+) ?([\w]+)? ?(default:(\w+))? ?')

def docstrparser(docstring):
    args={}
    argfun={}
    for line in docstring.split('\n'):
        if line and line[0]=='-':
            line = line.split("  ")[0]
            print(line)
            m=getgroups.match(line)
            print('grps',m.group(1),m.group(2),m.group(4))
            # lets read the groups 
            name = m.group(1)
            argfun[name] = eval(m.group(2)) if m.group(2) else bool # set type
            args[name] = argfun[name](m.group(4))   # bool(None) is false so this is fine

    return args, argfun


def argparser(args):
    result = {}
    carg = None
    cstuff = ''
    for e in args:
        if e[0]== '-':
            if carg:result[carg] = cstuff 
            carg = e[2:]
        else:
            cstuff+=e
    if carg:result[carg] = cstuff
    return result



def parse( docstring , args =  sys.argv[1:]):
    resargs, argfun = docstrparser(docstring)
    rawargs = argparser(args)
    for k,v in rawargs.items():
        if argfun.get(k,False) == bool: 
            resargs[k] = True
        elif k in argfun:
            resargs[k] = argfun[k](v)
        else:
            print(f'{k} is unknown but ill add it anyway... ')
            resargs[k] = True
    if resargs.get('h',False): # should work
        print(docstring)
    return resargs

if __name__ == '__main__':
    print(parse(doc))
