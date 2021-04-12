try:
    import pronomial
except ImportError:
    pronomial = None

from intentBox.coreference.base import CoreferenceSolver


class PronounCoreferenceSolver(CoreferenceSolver):

    @classmethod
    def solve_corefs(cls, text, lang="en"):
        if pronomial:
            return pronomial.replace_corefs(text, lang=lang)
        return text
