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
            replace_corefs("Members voted for John because they see him as a good leader."),
            "Members voted for John because Members see John as a good leader ."
        )
        self.assertEqual(
            replace_corefs("Leaders around the world say they stand for peace."),
            "Leaders around the world say Leaders stand for peace ."
        )
        self.assertEqual(
            replace_corefs("I have many friends. They are an important part of my life."),
            "I have many friends . friends are an important part of my life ."
        )
        # they + it
        self.assertEqual(
            replace_corefs("My neighbours just adopted a puppy. They care for it like a baby."),
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

        # it + who
        self.assertEqual(
            replace_corefs("London is the capital and most populous city of England and the United Kingdom. "
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
            replace_corefs("The sign was too far away for the boy to read it."),
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

    def test_hardcoded_postag_fixes(self):
        # failure cases
        # pos_tag confused Turn with a name, this specific use is corrected
        # manually when detected
        self.assertEqual(
            replace_corefs("Turn on the light and change it to blue"),
            "Turn on the light and change light to blue"
        )

    def test_known_failures(self):
        # understandable mistakes
        self.assertEqual(
            replace_corefs("Chris is very handsome. He is Australian. Elsa lives in Arendelle. He likes her."),
            "Chris is very handsome . Chris is Australian . Elsa lives in Arendelle . Chris likes Arendelle ."
            # "Chris is very handsome . Chris is Australian . Elsa lives in Arendelle . Chris likes Elsa ."
        )

        # TODO try to handle these
        self.assertEqual(
            replace_corefs( "Bob telephoned Jake to tell him that he lost the laptop."),
            "Bob telephoned Jake to tell Jake that Jake lost the laptop ."
            # Bob telephoned Jake to tell Jake that Bob lost the laptop .
        )


