import unittest
from pronomial import replace_corefs, word_tokenize, score_corefs


class TestCorefPT(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.lang = "pt"

    def test_female(self):
        # female only
        self.assertEqual(
            replace_corefs("A Ana gosta de cães. Ela tem dois",
                           lang=self.lang),
            "A Ana gosta de cães . Ana tem dois"
        )
        # female x2
        self.assertEqual(
            replace_corefs("a Ana disse á Maria que ela tem bom gosto",
                           lang=self.lang),
            "a Ana disse á Maria que Maria tem bom gosto"
        )
        # male + female
        self.assertEqual(
            replace_corefs("o João disse ao Joaquim que gosta da Ana. Ela "
                           "é bonita",
                           lang=self.lang),
            "o João disse ao Joaquim que gosta da Ana . Ana é bonita"
        )

    def test_male(self):
        # male only
        self.assertEqual(
            replace_corefs("o João gosta de gatos. Ele tem quatro",
                           lang=self.lang),
            "o João gosta de gatos . João tem quatro"
        )
        # male x2
        self.assertEqual(
            replace_corefs("o João disse ao Joaquim que ele está gordo",
                           lang=self.lang),
            "o João disse ao Joaquim que Joaquim está gordo"
        )

    def test_plural(self):
        # female noun from wordlist
        self.assertEqual(
            replace_corefs("As mulheres da ribeira do sado é que é, "
                           "Elas lavram a terra com as unhas dos pés",
                           lang=self.lang),
            "As mulheres da ribeira do sado é que é , mulheres lavram a terra com as unhas dos pés"
        )
        # male noun from wordlist
        self.assertEqual(
            replace_corefs("Os americanos foram á lua. Eles são fodidos",
                           lang=self.lang),
            "Os americanos foram á lua . americanos são fodidos"
        )

    def test_coreferences(self):

        # word indexes are used internally, but to make these tests human
        # friendly we are comparing actual words, note that in practice we
        # should work with token indexes
        def test_prediction(sentence, expected):
            tokens = word_tokenize(sentence)
            pred = score_corefs(sentence, lang="pt")
            matches = []
            for tok_idx, match in pred.items():
                tok = tokens[tok_idx]
                for tok2_idx, score in match.items():
                    tok2 = tokens[tok2_idx]
                    matches.append((tok, tok2, score))
            self.assertEqual(matches, expected)

        test_prediction(
            "o João disse ao Joaquim que ele está gordo",
            [('ele', 'João', 0.47),
             ('ele', 'Joaquim', 0.53)]
        )

        test_prediction(
            "a Ana disse á Maria que ela tem bom gosto",
            [('ela', 'Ana', 0.47),
             ('ela', 'Maria', 0.53)]
        )