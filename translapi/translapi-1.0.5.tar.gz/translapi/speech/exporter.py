from pydub import AudioSegment
import os
import wavio
def export(form,file):
    sound=AudioSegment.from_mp3(file)
    sound.export(os.path.splitext(file)[0]+form,format=form.replace('.',''))


