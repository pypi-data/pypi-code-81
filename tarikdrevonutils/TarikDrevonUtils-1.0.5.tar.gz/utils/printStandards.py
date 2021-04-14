from .glob_colors import*
import numpy as np


###########################################################################
#### defs : printing stuffs
def valsToStr(v,n=2,f='E'):
    if f == 'E':
        if n==1:
            vals = ['%.1E' %(val) for val in v];
        elif n==2:
            vals = ['%.2E' %(val) for val in v];
        else:
            vals = ['%.3E' %(val) for val in v]
    elif f=='f' :
        if n==1:
            vals = ['%.1f' %(val) for val in v];
        elif n==2:
            vals = ['%.2f' %(val) for val in v];
        else:
            vals = ['%.3f' %(val) for val in v]
    elif f=='d' :
        vals = ['%d' %(val) for val in v]
    else :
        return ''
    return  '[' + ', '.join(vals) + ']'

def printVals(v,f='E',prec=3):
    values = ''
    d  = {'f':0,'E':1}[f]
    xp = lambda x:[
        ['%.0f' %x,'%.1f' %x,'%.2f' %x,'%.3f' %x,'%.4f' %x ,'%.5f' %x,
         '%.6f' %x,'%.7f' %x,'%.8f' %x,'%.9f' %x,'%.10f' %x],
        ['%.0E' %x,'%.1E' %x,'%.2E' %x,'%.3E' %x,'%.4E' %x ,'%.5E' %x,
         '%.6E' %x,'%.7E' %x,'%.8E' %x,'%.9E' %x,'%.10E' %x]][d][prec]
    for val in v:
        if isinstance(val,int):
            values += '%-12d' %(val)
        elif isinstance(val,str):
            values += '%-12s' %(val)
        else:
            values += '%-12s' %(xp(val))
    print(values)

def printKeys(k):
    keys, line = ['','']
    strLine = '-'*12
    for key in k:
        keys   = keys + '%-12s' %(key)
        line   = line + strLine
    print(keys)
    print(line)


###########################################################################
#Tests
###########################################################################
def printList(k,v):
    keys ,values, line = ['','','']
    strLine = '-'*10
    for key,val in zip(k,v):
        keyStr = '%-10s' %(key) if val >0 else '%-11s' %(key)
        keys   = keys + keyStr
        line   = line + strLine
        values = values + '%.2E' %(val) + '  '
    print(keys)
    print(line)
    print(values)
def testPrint():
    l = ['mue(meV)', 'muh(meV)', 'Ne(/cm^3)', 'Nh(/cm^3)', 'G(/cm)']
    printKeys(l)
    printVals([0.5,-0.8, 1.0*pow(10.,19),5.0*pow(10.,16), -250.023])
    printVals([-0.5,-0.8, 1.0*pow(10.,19),+5.0*pow(10.,16), -250.023])
    printVals([0.5,0.8, -1.0*pow(10.,18),5.0*pow(10.,16), 250.023])
def testValsToStr():
    v = [1.25254,3.2545,5.245,5.02]
    print(valsToStr(v,1,'E'))
    print(valsToStr(v,2,'f'))
    print(valsToStr(v,3,'d'))
    print(valsToStr(v,4))
    print(valsToStr(v,3,''))

if __name__=='__main__':
    #testPrint()
    testValsToStr()
    print(green+__file__.split('/')[-1]+' success'+black)
