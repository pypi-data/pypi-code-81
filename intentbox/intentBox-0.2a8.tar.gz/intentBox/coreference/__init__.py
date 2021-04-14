from intentBox.utils import tokenize
from intentBox.coreference.pronoun_postags import PronounCoreferenceSolver as CoreferenceSolver


def replace_coreferences(text, smart=True, lang="en"):
    if smart:
        if lang.startswith("en"):
            from intentBox.lang.en import COREFERENCE_INDICATORS_EN
            indicators = COREFERENCE_INDICATORS_EN
        elif lang.startswith("pt"):
            from intentBox.lang.pt import COREFERENCE_INDICATORS_PT
            indicators = COREFERENCE_INDICATORS_PT
        else:
            indicators = []
        words = tokenize(text)
        should_solve = False
        for indicator in indicators:
            if indicator in words:
                should_solve = True
                break
        if not should_solve:
            return text
    solver = CoreferenceSolver(lang)
    solved = solver.replace_coreferences(text)
    if solved == text:
        return solver.replace_coreferences_with_context(text)
    return solved


