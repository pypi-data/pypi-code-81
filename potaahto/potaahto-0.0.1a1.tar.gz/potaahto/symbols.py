# standard imports
import re
import logging

logg = logging.getLogger().getChild(__name__)


re_camel = re.compile(r'([a-z0-9]+)([A-Z])')
re_snake = re.compile(r'([a-z0-9]+)_([A-Za-z])')
def snake_and_camel(src):
    src_normal = {}
    for k in src.keys():
        s_camel = ''
        s_snake = ''
        right_pos = 0
        for m in re_camel.finditer(k):
            g = m.group(0)
            s_snake += g[:len(g)-1]
            s_snake += '_' + g[len(g)-1].lower()
            right_pos = m.span()[1]
        s_snake += k[right_pos:]

        right_pos = 0
        for m in re_snake.finditer(k):
            g = m.group(0)
            s_camel += g[:len(g)-2]
            #s += '_' + g[len(g)-1].lower()
            s_camel += g[len(g)-1].upper()
            right_pos = m.span()[1]
        s_camel += k[right_pos:]

        src_normal[k] = src[k]
        #if s != k:
        if k != s_snake:
            logg.debug('adding snake {} for camel {}'.format(s_snake, k))
            src_normal[s_snake] = src[k]

        if k != s_camel:
            logg.debug('adding camel {} for snake {}'.format(s_camel, k))
            src_normal[s_camel] = src[k]

    return src_normal


