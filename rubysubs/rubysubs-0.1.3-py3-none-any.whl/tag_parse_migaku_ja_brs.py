from enum import Enum

# Entries: (main_text, ruby_text, following_text, accent_list, dictionary_form)

def parse_migaku(text):
    lines = []

    for l in text.split('\n'):
        parts = []

        last = 0
        
        while True:
            i = l.find('[', last)
            if i < 0:
                break
            j = l.find(']', i+1)
            if j < 0:
                break
            
            k = l.rfind(' ', last, i)

            if last < k:
                parts.append( (l[last:k], '', '', [], None) )

            k = max(last, k+1)

            m = l.find(' ', j+1)
            if m < 0:
                m = len(l)

            bracket_parts = l[i+1:j].split(';')
            ruby_text = ''
            accent_list = []
            dictionary_form = None

            bracket_parts_1 = bracket_parts[0].replace('、', ',').split(',')  # Replace to support both browser and anki syntax
            ruby_text = bracket_parts_1[0]
            if len(bracket_parts_1) >= 2:
                dictionary_form = bracket_parts_1[1]
            if len(bracket_parts) >= 2:
                accent_list = bracket_parts[1].split(',')

            parts.append( (l[k:i], ruby_text, l[j+1:m], accent_list, dictionary_form) )

            last = m+1

        if last < len(l):
            parts.append( (l[last:len(l)], '', '', [], None) )

        lines.append(parts)

    return lines


class Mode(Enum):
    KANJI = 0,
    KANJI_READING = 1,
    READING = 2,

    @classmethod
    def from_string(cls, key):
        associations = {
            'kanji':        cls.KANJI,
            'kanjireading': cls.KANJI_READING,
            'reading':      cls.READING,
            'furigana':     cls.KANJI_READING,
            'kana':         cls.READING,
        }
        return associations.get(key.lower(), cls.KANJI_READING)



def migaku_to_ruby(parsed_lines, pitch_highlighting=True, mode=Mode.KANJI_READING):

    coloring = {
        'h': '005CE6',  # Heiban
        'a': 'E60000',  # Atamadaka
        'n': 'E68A00',  # Nakadaka
        'o': '00802B',  # Odaka
        'k': 'AC00E6',  # Kifuku
    }

    ret = []

    for l in parsed_lines:
        retl = []

        for (main_text, ruby_text, following_text, accent_list, dictionary_form) in l:
            co = ''
            cc = ''
            if pitch_highlighting and len(accent_list) and len(accent_list[0]):
                color = coloring.get(accent_list[0][0])
                if color:
                    co = '{\\c&H' + color[4:6] + color[2:4] + color[0:2] + '&}'
                    cc = '{\\c}'
            
            if mode == Mode.KANJI and main_text:
                retl.append( (co + main_text + cc, '') )
            elif mode == Mode.READING:
                txt = ruby_text
                if not txt:
                    txt = main_text
                if txt:
                    retl.append( (co + txt + cc, '') )
            else:
                if main_text or ruby_text:
                    p1 = main_text
                    p2 = ruby_text
                    if main_text: p1 = co + main_text + cc
                    if ruby_text: p2 = co + ruby_text + cc
                    retl.append( (p1, p2) )

            if following_text:
                retl.append( (co + following_text + cc, '') )

        ret.append(retl)

    return ret


def parse(text, pitch_highlighting=True, mode=Mode.KANJI_READING):
    migaku_parsed = parse_migaku(text)
    return migaku_to_ruby(migaku_parsed, pitch_highlighting, mode)


def args_from_strings(in_args):
    out_args = [True, Mode.KANJI_READING]

    if len(in_args) >= 1:
        out_args[0] = in_args[0].lower() not in ['no', 'n', 'false', 'f', '0']

    if len(in_args) >= 2:
        out_args[1] = Mode.from_string(in_args[1])

    return out_args


def parser_from_string_args(in_args):
    args = args_from_strings(in_args)
    return (lambda text: parse(text, *args))


def main():
    import sys

    if len(sys.argv) not in [2]:
        print('Usage: %s <text>' % sys.argv[0])
        sys.exit(1)

    migaku_parsed = parse_migaku(sys.argv[1])
    parsed = migaku_to_ruby(migaku_parsed)

    print(migaku_parsed)
    print(parsed)

    sys.exit(0)


if __name__ == "__main__":
    main()
