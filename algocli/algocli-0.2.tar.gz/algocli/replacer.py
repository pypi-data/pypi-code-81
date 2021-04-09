'''
Character replacer for algocli raw code lines
written by Emanuel Ramirez (emanuel2718@gmail.com)
'''

# Keys are the unwanted tags and values are the replacement for each tag
BASIC_TOKENS = {
    '}</lang>': '}',
    '}</pre>': '}',
    '</pre>': '',
    '<pre': '',
    '{{works': '',
    '=={{header': '',
    '<br>': '',
    '{{out}}': '',
    '{{libheader': '',
    'Output:': '',
    "'''Output'''": '',
    '{{Out}}': '\n=== Output ===',
    '{{trans': '',
    'Usage:': "\n\n'''How to use'''"
}

def get_replacement_line(curr_line):
    ''' Returns the formatted line without the html and wiki tags

    :param: line: current line of wiki-text from rosseta code
    :return cleaned line of code without the unwanted tags
    '''
    if curr_line.startswith('<lang') and curr_line.endswith('</lang>'):
        return curr_line.split('>', 1)[-1].split('<')[0]

    elif curr_line.startswith('<lang'):
        return curr_line.split('>', 1)[-1]

    elif curr_line.endswith('</lang>'):
        return curr_line.partition('</')[0]

    elif curr_line.startswith('==='):
        return f'\n{curr_line}\n'

    elif curr_line.startswith("'''"):
        return f'\n{curr_line}'

    elif curr_line.startswith('{{out}}Output'):
        return f'\n=== {curr_line.rpartition("}")[-1]} ==='

    elif curr_line.endswith('.'):
        return f'{curr_line}\n'

    else:
        for key in BASIC_TOKENS.keys():
            if curr_line.startswith(key) or curr_line.endswith(key):
                return BASIC_TOKENS[key]

    return curr_line


if __name__ == '__main__':
     print('This file is not intended to be called by the user. See algocli --help')
