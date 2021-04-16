import gtts
import gtts.lang
import langdetect
import os
import vlc
from . import exporter
class Speaker:
    def __init__(self,phrase,hard=False,lang=None):
        self.hard=hard
        if hard:
            if not lang:
                raise ValueError('Hard mode without language')
            self.lang=lang
        else:
            self.langs=langdetect.detect_langs(phrase)
            self.lang='en'
            for s in self.langs:
                if s.lang in gtts.lang.tts_langs():
                    self.lang=s.lang
                    break                
        self.g=gtts.gTTS(phrase)
        self.g.lang=self.lang
    def say(self):
        error=False
        try:
            self.g.save('sample.mp3')
        except gtts.tts.gTTSError:
            error=True
        if error:
            if not self.hard:
                raise ValueError(f'Fatal::no sample speech for detected language "{self.lang}"')
            raise ValueError(f'No sample speech for language "{self.lang}"')
        media=vlc.MediaPlayer('sample.mp3')
        media.play()
    def save(self,where):
        self.g.save(os.path.splitext(where)[0]+'.mp3')
        exporter.export(os.path.splitext(where)[1],os.path.splitext(where)[0]+'.mp3')
    def cleanup(self):
        try:
            os.remove('sample.mp3')
        except FileNotFoundError:pass
