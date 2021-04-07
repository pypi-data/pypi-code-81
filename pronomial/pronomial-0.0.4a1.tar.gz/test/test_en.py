import unittest
from pronomial import replace_corefs


class TestCorefEN(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.lang = "en"

    def test_female(self):
        self.assertEqual(
            replace_corefs("Inês said she loves me!"),
            "Inês said Inês loves me !"
        )
        self.assertEqual(
            replace_corefs("Bob threatened to kill Alice to make her pay "
                           "her debts"),
            "Bob threatened to kill Alice to make Alice pay Alice debts"
        )

    def test_male(self):
        self.assertEqual(
            replace_corefs("Jack is one of the top candidates in "
                           "the elections. His ideas are unique compared to "
                           "Bob's."),
            "Jack is one of the top candidates in the elections . Jack ideas are unique compared to Bob 's ."
        )
        self.assertEqual(
            replace_corefs("I voted for Elon because he is clear about his "
                           "values. His ideas represent a majority of the "
                           "nation. He is better than Jack."),
            "I voted for Elon because Elon is clear about Elon values ."
            " Elon ideas represent a majority of the nation ."
            " Elon is better than Jack ."
        )

    def test_plural(self):
        self.assertEqual(
            replace_corefs(
                "Members voted for John because they see him as a good leader."),
            "Members voted for John because Members see John as a good leader ."
        )
        self.assertEqual(
            replace_corefs(
                "Leaders around the world say they stand for peace."),
            "Leaders around the world say Leaders stand for peace ."
        )
        self.assertEqual(
            replace_corefs(
                "I have many friends. They are an important part of my life."),
            "I have many friends . friends are an important part of my life ."
        )
        # they + it
        self.assertEqual(
            replace_corefs(
                "My neighbours just adopted a puppy. They care for it like a baby."),
            "My neighbours just adopted a puppy . neighbours care for puppy like a baby ."
        )

    def test_it(self):
        self.assertEqual(
            replace_corefs("My neighbors have a cat. It has a bushy tail."),
            "My neighbors have a cat . cat has a bushy tail ."
        )
        self.assertEqual(
            replace_corefs("Here is the book now take it."),
            "Here is the book now take book ."
        )
        self.assertEqual(
            replace_corefs("Dog is man's best friend. It is always loyal."),
            "Dog is man 's best friend . Dog is always loyal ."
        )
        self.assertEqual(
            replace_corefs("is the light turned on? turn it off"),
            "is the light turned on ? turn light off"
        )
        self.assertEqual(
            replace_corefs("Turn off the light and change it to blue"),
            "Turn off the light and change light to blue"
        )

        # it + who
        self.assertEqual(
            replace_corefs(
                "London is the capital and most populous city of England and the United Kingdom. "
                "Standing on the River Thames in the south east of the island of Great Britain, "
                "London has been a major settlement for two millennia. "
                "It was founded by the Romans, who named it Londinium."),
            "London is the capital and most populous city of England and the United Kingdom . "
            "Standing on the River Thames in the south east of the island of Great Britain , "
            "London has been a major settlement for two millennia . "
            "London was founded by the Romans , Romans named London Londinium ."
        )

    def test_dictionary_words(self):
        # harcoded wordlists that map words to gendered pronouns
        # boy -> male
        self.assertEqual(
            replace_corefs(
                "The sign was too far away for the boy to read it."),
            "The sign was too far away for the boy to read sign ."
        )
        # girl -> female
        self.assertEqual(
            replace_corefs("The girl said she would take the trash out."),
            "The girl said girl would take the trash out ."
        )
        # mom -> female
        self.assertEqual(
            replace_corefs("call Mom. tell her to buy eggs. tell her to buy "
                           "coffee. tell her to buy milk"),
            "call Mom . tell Mom to buy eggs . tell Mom to buy coffee . tell Mom to buy milk"
        )
        # dad -> male
        self.assertEqual(
            replace_corefs("call dad. tell him to buy bacon. tell him to buy "
                           "coffee. tell him to buy beer"),
            "call dad . tell dad to buy bacon . tell dad to buy coffee . tell dad to buy beer"
        )

    def test_hardcoded_postag_fixes(self):
        # failure cases
        # pos_tag confused Turn with a name, this specific use is corrected
        # manually when detected
        self.assertEqual(
            replace_corefs("Turn on the light and change it to blue"),
            "Turn on the light and change light to blue"
        )

    def test_ambiguous(self):
        # understandable mistakes
        self.assertEqual(
            replace_corefs(
                "Chris is very handsome. He is Australian. Elsa lives in Arendelle. He likes her."),
            "Chris is very handsome . Chris is Australian . Elsa lives in Arendelle . Chris likes Arendelle ."
            # "Chris is very handsome . Chris is Australian . Elsa lives in Arendelle . Chris likes Elsa ."
        )

    def test_with(self):
        # "with her/him/them" will select first male/female/plural noun
        # instead of last seen
        self.assertEqual(
            replace_corefs("Kevin invited Bob to go with him to "
                           "his favorite fishing spot"),
            "Kevin invited Bob to go with Kevin to Bob favorite fishing spot"
        )
        self.assertEqual(
            replace_corefs("Alice invited Marcia to go with her to "
                           "their favorite store"),
            "Alice invited Marcia to go with Alice to Marcia favorite store"
        )
        self.assertEqual(
            replace_corefs("The Martians invited the Venusians to go with "
                           "them to Pluto"),
            "The Martians invited the Venusians to go with Martians to Pluto"
        )

    def test_that(self):
        # "that her/he/they" will select first male/female/plural noun
        # instead of last seen
        self.assertEqual(
            replace_corefs(
                "Bob telephoned Jake to tell him that he lost the laptop."),
            "Bob telephoned Jake to tell Jake that Bob lost the laptop ."
        )
        self.assertEqual(
            replace_corefs("Ana telephoned Alice to tell her that she lost "
                           "the bus"),
            "Ana telephoned Alice to tell Alice that Ana lost the bus"
        )
        self.assertEqual(
            replace_corefs("The Martians told the Venusians that they used "
                           "to have an ocean"),
            "The Martians told the Venusians that Martians used to have an ocean"
        )

