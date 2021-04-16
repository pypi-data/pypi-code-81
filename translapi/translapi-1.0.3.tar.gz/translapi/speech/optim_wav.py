import wavio
import os
from . import exporter
def optim(file):
    name,ext=os.path.splitext(file)
    newwav=name+'.wav'
    if ext not in ('.wav','.mp3'):
        raise ValueError('File must be .wav or .mp3 format')
    if ext == '.mp3':
        exporter.export('.wav',newwav)
    np=wavio.read(file).data
    r=wavio.read(file).rate
    wavio.save(newwav,data,rate)
