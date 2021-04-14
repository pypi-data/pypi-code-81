from markovjson.mkov import MarkovJson


class MarkovCharJson(MarkovJson):
    def tokenize(self, text, wildcards=False):
        sequence = list(text)
        if wildcards:
            sequence = self.replace_wildcards(sequence)
        if self.reverse_modelling:
            sequence.reverse()
        return sequence

    def generate_string(self, *args, **kwargs):
        seq = self.generate_sequence(*args, **kwargs)
        s = "".join([s for s in seq if
                        s != self.START_OF_SEQ and s != self.END_OF_SEQ])
        if self.reverse_modelling:
            return s[::-1]
        return s


class MarkovWordJson(MarkovJson):
    def generate_string(self, *args, **kwargs):
        seq = self.generate_sequence(*args, **kwargs)
        s = " ".join([s for s in seq if
                         s != self.START_OF_SEQ and s != self.END_OF_SEQ])
        if self.reverse_modelling:
            return s[::-1]
        return s


class MarkovNLPJson(MarkovWordJson):
    def __init__(self, normalize=False, postag=True, wildcard_postags=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.normalize = normalize
        self.postag = postag
        self.wildcard_postags = wildcard_postags or []

    def tokenize(self, text, wildcards=False):
        try:
            from markovjson.nlp import pos_tag, normalize
        except ImportError:
            print("pip install nltk")
            raise
        if self.normalize:
            text = normalize(text)

        if self.postag:
            sequence = [f"{p[0]} [/POSTAG={p[1]}]" for p in pos_tag(text)]
        else:
            return super().tokenize(text, wildcards)
        if wildcards:
            sequence = self.replace_wildcards(sequence)
        return sequence

    def replace_wildcards(self, sequence):
        for idx, word in enumerate(sequence):
            for tag in self.wildcard_postags:
                if f"[/POSTAG={tag}]" in word:
                    sequence[idx] = f"[/POSTAG={tag}]"
                elif word not in self.tokens:
                    sequence[idx] = self.WILDCARD_SEQ
        if self.reverse_modelling:
            sequence.reverse()
        return sequence

    def generate_string(self, *args, **kwargs):
        seq = self.generate_sequence(*args, **kwargs)
        s = " ".join([s.split(" ")[0] for s in seq if
                         s != self.START_OF_SEQ and s != self.END_OF_SEQ])
        if self.reverse_modelling:
            return s[::-1]
        return s


