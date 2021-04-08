import unittest
from pronomial import replace_corefs


class TestCorefPT(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.lang = "es"

    def test_female(self):
        self.assertEqual(
            replace_corefs("A Ana gosta de cães. Ella tem dois",
                           lang=self.lang),
            "A Ana gosta de cães . Ana tem dois"
        )

    def test_male(self):
        self.assertEqual(
            replace_corefs("o João gosta de gatos. Ello tem quatro",
                           lang=self.lang),
            "o João gosta de gatos . João tem quatro"
        )

    def test_plural(self):

        self.assertEqual(
            replace_corefs("Los americanos foram á lua. Ellos são fodidos",
                           lang=self.lang),
            "Los americanos foram á lua . americanos são fodidos"
        )