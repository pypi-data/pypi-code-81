import unittest
from pronomial import replace_corefs


class TestCorefPT(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.lang = "pt"

    def test_female(self):
        self.assertEqual(
            replace_corefs("A Ana gosta de cães. Ela tem dois", lang="pt"),
            "A Ana gosta de cães . Ana tem dois"
        )

    def test_male(self):
        self.assertEqual(
            replace_corefs("o João gosta de gatos. Ele tem quatro", lang="pt"),
            "o João gosta de gatos . João tem quatro"
        )

    def test_plural(self):
        self.assertEqual(
            replace_corefs("As mulheres da ribeira do sado é que é, "
                           "Elas lavram a terra com as unhas dos pés",
                           lang="pt"),
            "As mulheres da ribeira do sado é que é , mulheres lavram a terra com as unhas dos pés"
        )
        self.assertEqual(
            replace_corefs("Os americanos foram á lua. Eles são fodidos",
                           lang="pt"),
            "Os americanos foram á lua . americanos são fodidos"
        )