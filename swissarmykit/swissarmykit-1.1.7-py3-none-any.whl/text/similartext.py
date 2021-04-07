import difflib
# import textdistance

# https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings

class SimilarText:

    def __init__(self):
        pass


    def similar(self):
        pass

    @staticmethod
    def diff_ratio(text, text2):
        if isinstance(text2, dict):
            values = {t:SimilarText.diff_ratio(text, t) for t in list(set(text2.values()))}  # {pre-processing name for easy to compare: ratio}

            x = {}
            for k in text2.keys():
                x[k] = values.get(text2.get(k))
            return sorted(x.items(), key=lambda kv: kv[1], reverse=True)

        if isinstance(text2, list):
            x = {t:SimilarText.diff_ratio(text, t) for t in text2}
            return sorted(x.items(), key=lambda kv: kv[1], reverse=True)

        return difflib.SequenceMatcher(None, text, text2).ratio()

if __name__ == '__main__':
    s = SimilarText()
    print(s.diff_ratio('hello world', 'hello'))
    print(s.diff_ratio('hello world', 'hello_orld'))
    print(s.diff_ratio('hello world', 'hello  world'))
    print(s.diff_ratio('hello world', 'hello.world'))


    print(s.diff_ratio('hello world', ['hello.world', 'hello  world', 'ello-wordl']))
