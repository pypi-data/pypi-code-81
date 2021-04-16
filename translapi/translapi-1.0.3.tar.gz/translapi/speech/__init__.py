from . import tts
import os
def say(phrase,lang=None,hard=False):
    s=tts.Speaker(phrase,hard=hard,lang=lang)
    s.say()
    return s
def save(phrase,where,lang=None,hard=False):
    s=tts.Speaker(phrase,hard=hard,lang=lang)
    s.save(where)
    s.cleanup()
    
    return s

