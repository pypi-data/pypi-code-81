def parse(text):
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
                parts.append( (l[last:k], '') )

            k = max(last, k+1)

            parts.append( (l[k:i], l[i+1:j]) )

            last = j+1

        if last < len(l):
            parts.append( (l[last:len(l)], '') )

        lines.append(parts)

    return lines


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print('Usage: %s <text>' % sys.argv[0])
        sys.exit(1)

    print(parse(sys.argv[1]))

    sys.exit(0)
