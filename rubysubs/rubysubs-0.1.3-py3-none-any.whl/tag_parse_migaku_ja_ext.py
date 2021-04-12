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

            bracket_parts_1 = bracket_parts[0].split('、')
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


def migaku_to_ruby(parsed_lines):

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
            if len(accent_list) and len(accent_list[0]):
                color = coloring.get(accent_list[0][0])
                if color:
                    co = '{\\c&H' + color[4:6] + color[2:4] + color[0:2] + '&}'
                    cc = '{\\c}'
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


def parse(text):
    return migaku_to_ruby(parse_migaku(text))


def main():
    import sys

    if len(sys.argv) != 2:
        print('Usage: %s <text>' % sys.argv[0])
        sys.exit(1)

    migaku_parsed = parse_migaku(sys.argv[1])
    parsed = migaku_to_ruby(migaku_parsed)

    print(migaku_parsed)
    print(parsed)

    sys.exit(0)


if __name__ == "__main__":
    main()
