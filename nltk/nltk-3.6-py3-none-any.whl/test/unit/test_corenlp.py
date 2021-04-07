# -*- coding: utf-8 -*-

"""
Mock test for Stanford CoreNLP wrappers.
"""

from unittest import TestCase
from unittest.mock import MagicMock

from nltk.tree import Tree
from nltk.parse import corenlp


class TestTokenizerAPI(TestCase):
    def test_tokenize(self):
        corenlp_tokenizer = corenlp.CoreNLPParser()

        api_return_value = {
            u'sentences': [
                {
                    u'index': 0,
                    u'tokens': [
                        {
                            u'after': u' ',
                            u'before': u'',
                            u'characterOffsetBegin': 0,
                            u'characterOffsetEnd': 4,
                            u'index': 1,
                            u'originalText': u'Good',
                            u'word': u'Good',
                        },
                        {
                            u'after': u' ',
                            u'before': u' ',
                            u'characterOffsetBegin': 5,
                            u'characterOffsetEnd': 12,
                            u'index': 2,
                            u'originalText': u'muffins',
                            u'word': u'muffins',
                        },
                        {
                            u'after': u' ',
                            u'before': u' ',
                            u'characterOffsetBegin': 13,
                            u'characterOffsetEnd': 17,
                            u'index': 3,
                            u'originalText': u'cost',
                            u'word': u'cost',
                        },
                        {
                            u'after': u'',
                            u'before': u' ',
                            u'characterOffsetBegin': 18,
                            u'characterOffsetEnd': 19,
                            u'index': 4,
                            u'originalText': u'$',
                            u'word': u'$',
                        },
                        {
                            u'after': u'\n',
                            u'before': u'',
                            u'characterOffsetBegin': 19,
                            u'characterOffsetEnd': 23,
                            u'index': 5,
                            u'originalText': u'3.88',
                            u'word': u'3.88',
                        },
                        {
                            u'after': u' ',
                            u'before': u'\n',
                            u'characterOffsetBegin': 24,
                            u'characterOffsetEnd': 26,
                            u'index': 6,
                            u'originalText': u'in',
                            u'word': u'in',
                        },
                        {
                            u'after': u' ',
                            u'before': u' ',
                            u'characterOffsetBegin': 27,
                            u'characterOffsetEnd': 30,
                            u'index': 7,
                            u'originalText': u'New',
                            u'word': u'New',
                        },
                        {
                            u'after': u'',
                            u'before': u' ',
                            u'characterOffsetBegin': 31,
                            u'characterOffsetEnd': 35,
                            u'index': 8,
                            u'originalText': u'York',
                            u'word': u'York',
                        },
                        {
                            u'after': u'  ',
                            u'before': u'',
                            u'characterOffsetBegin': 35,
                            u'characterOffsetEnd': 36,
                            u'index': 9,
                            u'originalText': u'.',
                            u'word': u'.',
                        },
                    ],
                },
                {
                    u'index': 1,
                    u'tokens': [
                        {
                            u'after': u' ',
                            u'before': u'  ',
                            u'characterOffsetBegin': 38,
                            u'characterOffsetEnd': 44,
                            u'index': 1,
                            u'originalText': u'Please',
                            u'word': u'Please',
                        },
                        {
                            u'after': u' ',
                            u'before': u' ',
                            u'characterOffsetBegin': 45,
                            u'characterOffsetEnd': 48,
                            u'index': 2,
                            u'originalText': u'buy',
                            u'word': u'buy',
                        },
                        {
                            u'after': u'\n',
                            u'before': u' ',
                            u'characterOffsetBegin': 49,
                            u'characterOffsetEnd': 51,
                            u'index': 3,
                            u'originalText': u'me',
                            u'word': u'me',
                        },
                        {
                            u'after': u' ',
                            u'before': u'\n',
                            u'characterOffsetBegin': 52,
                            u'characterOffsetEnd': 55,
                            u'index': 4,
                            u'originalText': u'two',
                            u'word': u'two',
                        },
                        {
                            u'after': u' ',
                            u'before': u' ',
                            u'characterOffsetBegin': 56,
                            u'characterOffsetEnd': 58,
                            u'index': 5,
                            u'originalText': u'of',
                            u'word': u'of',
                        },
                        {
                            u'after': u'',
                            u'before': u' ',
                            u'characterOffsetBegin': 59,
                            u'characterOffsetEnd': 63,
                            u'index': 6,
                            u'originalText': u'them',
                            u'word': u'them',
                        },
                        {
                            u'after': u'\n',
                            u'before': u'',
                            u'characterOffsetBegin': 63,
                            u'characterOffsetEnd': 64,
                            u'index': 7,
                            u'originalText': u'.',
                            u'word': u'.',
                        },
                    ],
                },
                {
                    u'index': 2,
                    u'tokens': [
                        {
                            u'after': u'',
                            u'before': u'\n',
                            u'characterOffsetBegin': 65,
                            u'characterOffsetEnd': 71,
                            u'index': 1,
                            u'originalText': u'Thanks',
                            u'word': u'Thanks',
                        },
                        {
                            u'after': u'',
                            u'before': u'',
                            u'characterOffsetBegin': 71,
                            u'characterOffsetEnd': 72,
                            u'index': 2,
                            u'originalText': u'.',
                            u'word': u'.',
                        },
                    ],
                },
            ]
        }
        corenlp_tokenizer.api_call = MagicMock(return_value=api_return_value)

        input_string = "Good muffins cost $3.88\nin New York.  Please buy me\ntwo of them.\nThanks."

        expected_output = [
            u'Good',
            u'muffins',
            u'cost',
            u'$',
            u'3.88',
            u'in',
            u'New',
            u'York',
            u'.',
            u'Please',
            u'buy',
            u'me',
            u'two',
            u'of',
            u'them',
            u'.',
            u'Thanks',
            u'.',
        ]

        tokenized_output = list(corenlp_tokenizer.tokenize(input_string))

        corenlp_tokenizer.api_call.assert_called_once_with(
            'Good muffins cost $3.88\nin New York.  Please buy me\ntwo of them.\nThanks.',
            properties={'annotators': 'tokenize,ssplit'},
        )
        self.assertEqual(expected_output, tokenized_output)


class TestTaggerAPI(TestCase):
    def test_pos_tagger(self):
        corenlp_tagger = corenlp.CoreNLPParser(tagtype='pos')

        api_return_value = {
            u'sentences': [
                {
                    u'basicDependencies': [
                        {
                            u'dep': u'ROOT',
                            u'dependent': 1,
                            u'dependentGloss': u'What',
                            u'governor': 0,
                            u'governorGloss': u'ROOT',
                        },
                        {
                            u'dep': u'cop',
                            u'dependent': 2,
                            u'dependentGloss': u'is',
                            u'governor': 1,
                            u'governorGloss': u'What',
                        },
                        {
                            u'dep': u'det',
                            u'dependent': 3,
                            u'dependentGloss': u'the',
                            u'governor': 4,
                            u'governorGloss': u'airspeed',
                        },
                        {
                            u'dep': u'nsubj',
                            u'dependent': 4,
                            u'dependentGloss': u'airspeed',
                            u'governor': 1,
                            u'governorGloss': u'What',
                        },
                        {
                            u'dep': u'case',
                            u'dependent': 5,
                            u'dependentGloss': u'of',
                            u'governor': 8,
                            u'governorGloss': u'swallow',
                        },
                        {
                            u'dep': u'det',
                            u'dependent': 6,
                            u'dependentGloss': u'an',
                            u'governor': 8,
                            u'governorGloss': u'swallow',
                        },
                        {
                            u'dep': u'compound',
                            u'dependent': 7,
                            u'dependentGloss': u'unladen',
                            u'governor': 8,
                            u'governorGloss': u'swallow',
                        },
                        {
                            u'dep': u'nmod',
                            u'dependent': 8,
                            u'dependentGloss': u'swallow',
                            u'governor': 4,
                            u'governorGloss': u'airspeed',
                        },
                        {
                            u'dep': u'punct',
                            u'dependent': 9,
                            u'dependentGloss': u'?',
                            u'governor': 1,
                            u'governorGloss': u'What',
                        },
                    ],
                    u'enhancedDependencies': [
                        {
                            u'dep': u'ROOT',
                            u'dependent': 1,
                            u'dependentGloss': u'What',
                            u'governor': 0,
                            u'governorGloss': u'ROOT',
                        },
                        {
                            u'dep': u'cop',
                            u'dependent': 2,
                            u'dependentGloss': u'is',
                            u'governor': 1,
                            u'governorGloss': u'What',
                        },
                        {
                            u'dep': u'det',
                            u'dependent': 3,
                            u'dependentGloss': u'the',
                            u'governor': 4,
                            u'governorGloss': u'airspeed',
                        },
                        {
                            u'dep': u'nsubj',
                            u'dependent': 4,
                            u'dependentGloss': u'airspeed',
                            u'governor': 1,
                            u'governorGloss': u'What',
                        },
                        {
                            u'dep': u'case',
                            u'dependent': 5,
                            u'dependentGloss': u'of',
                            u'governor': 8,
                            u'governorGloss': u'swallow',
                        },
                        {
                            u'dep': u'det',
                            u'dependent': 6,
                            u'dependentGloss': u'an',
                            u'governor': 8,
                            u'governorGloss': u'swallow',
                        },
                        {
                            u'dep': u'compound',
                            u'dependent': 7,
                            u'dependentGloss': u'unladen',
                            u'governor': 8,
                            u'governorGloss': u'swallow',
                        },
                        {
                            u'dep': u'nmod:of',
                            u'dependent': 8,
                            u'dependentGloss': u'swallow',
                            u'governor': 4,
                            u'governorGloss': u'airspeed',
                        },
                        {
                            u'dep': u'punct',
                            u'dependent': 9,
                            u'dependentGloss': u'?',
                            u'governor': 1,
                            u'governorGloss': u'What',
                        },
                    ],
                    u'enhancedPlusPlusDependencies': [
                        {
                            u'dep': u'ROOT',
                            u'dependent': 1,
                            u'dependentGloss': u'What',
                            u'governor': 0,
                            u'governorGloss': u'ROOT',
                        },
                        {
                            u'dep': u'cop',
                            u'dependent': 2,
                            u'dependentGloss': u'is',
                            u'governor': 1,
                            u'governorGloss': u'What',
                        },
                        {
                            u'dep': u'det',
                            u'dependent': 3,
                            u'dependentGloss': u'the',
                            u'governor': 4,
                            u'governorGloss': u'airspeed',
                        },
                        {
                            u'dep': u'nsubj',
                            u'dependent': 4,
                            u'dependentGloss': u'airspeed',
                            u'governor': 1,
                            u'governorGloss': u'What',
                        },
                        {
                            u'dep': u'case',
                            u'dependent': 5,
                            u'dependentGloss': u'of',
                            u'governor': 8,
                            u'governorGloss': u'swallow',
                        },
                        {
                            u'dep': u'det',
                            u'dependent': 6,
                            u'dependentGloss': u'an',
                            u'governor': 8,
                            u'governorGloss': u'swallow',
                        },
                        {
                            u'dep': u'compound',
                            u'dependent': 7,
                            u'dependentGloss': u'unladen',
                            u'governor': 8,
                            u'governorGloss': u'swallow',
                        },
                        {
                            u'dep': u'nmod:of',
                            u'dependent': 8,
                            u'dependentGloss': u'swallow',
                            u'governor': 4,
                            u'governorGloss': u'airspeed',
                        },
                        {
                            u'dep': u'punct',
                            u'dependent': 9,
                            u'dependentGloss': u'?',
                            u'governor': 1,
                            u'governorGloss': u'What',
                        },
                    ],
                    u'index': 0,
                    u'parse': u'(ROOT\n  (SBARQ\n    (WHNP (WP What))\n    (SQ (VBZ is)\n      (NP\n        (NP (DT the) (NN airspeed))\n        (PP (IN of)\n          (NP (DT an) (NN unladen) (NN swallow)))))\n    (. ?)))',
                    u'tokens': [
                        {
                            u'after': u' ',
                            u'before': u'',
                            u'characterOffsetBegin': 0,
                            u'characterOffsetEnd': 4,
                            u'index': 1,
                            u'lemma': u'what',
                            u'originalText': u'What',
                            u'pos': u'WP',
                            u'word': u'What',
                        },
                        {
                            u'after': u' ',
                            u'before': u' ',
                            u'characterOffsetBegin': 5,
                            u'characterOffsetEnd': 7,
                            u'index': 2,
                            u'lemma': u'be',
                            u'originalText': u'is',
                            u'pos': u'VBZ',
                            u'word': u'is',
                        },
                        {
                            u'after': u' ',
                            u'before': u' ',
                            u'characterOffsetBegin': 8,
                            u'characterOffsetEnd': 11,
                            u'index': 3,
                            u'lemma': u'the',
                            u'originalText': u'the',
                            u'pos': u'DT',
                            u'word': u'the',
                        },
                        {
                            u'after': u' ',
                            u'before': u' ',
                            u'characterOffsetBegin': 12,
                            u'characterOffsetEnd': 20,
                            u'index': 4,
                            u'lemma': u'airspeed',
                            u'originalText': u'airspeed',
                            u'pos': u'NN',
                            u'word': u'airspeed',
                        },
                        {
                            u'after': u' ',
                            u'before': u' ',
                            u'characterOffsetBegin': 21,
                            u'characterOffsetEnd': 23,
                            u'index': 5,
                            u'lemma': u'of',
                            u'originalText': u'of',
                            u'pos': u'IN',
                            u'word': u'of',
                        },
                        {
                            u'after': u' ',
                            u'before': u' ',
                            u'characterOffsetBegin': 24,
                            u'characterOffsetEnd': 26,
                            u'index': 6,
                            u'lemma': u'a',
                            u'originalText': u'an',
                            u'pos': u'DT',
                            u'word': u'an',
                        },
                        {
                            u'after': u' ',
                            u'before': u' ',
                            u'characterOffsetBegin': 27,
                            u'characterOffsetEnd': 34,
                            u'index': 7,
                            u'lemma': u'unladen',
                            u'originalText': u'unladen',
                            u'pos': u'JJ',
                            u'word': u'unladen',
                        },
                        {
                            u'after': u' ',
                            u'before': u' ',
                            u'characterOffsetBegin': 35,
                            u'characterOffsetEnd': 42,
                            u'index': 8,
                            u'lemma': u'swallow',
                            u'originalText': u'swallow',
                            u'pos': u'VB',
                            u'word': u'swallow',
                        },
                        {
                            u'after': u'',
                            u'before': u' ',
                            u'characterOffsetBegin': 43,
                            u'characterOffsetEnd': 44,
                            u'index': 9,
                            u'lemma': u'?',
                            u'originalText': u'?',
                            u'pos': u'.',
                            u'word': u'?',
                        },
                    ],
                }
            ]
        }
        corenlp_tagger.api_call = MagicMock(return_value=api_return_value)

        input_tokens = 'What is the airspeed of an unladen swallow ?'.split()
        expected_output = [
            ('What', 'WP'),
            ('is', 'VBZ'),
            ('the', 'DT'),
            ('airspeed', 'NN'),
            ('of', 'IN'),
            ('an', 'DT'),
            ('unladen', 'JJ'),
            ('swallow', 'VB'),
            ('?', '.'),
        ]
        tagged_output = corenlp_tagger.tag(input_tokens)

        corenlp_tagger.api_call.assert_called_once_with(
            'What is the airspeed of an unladen swallow ?',
            properties={
                'ssplit.isOneSentence': 'true',
                'annotators': 'tokenize,ssplit,pos',
            },
        )
        self.assertEqual(expected_output, tagged_output)

    def test_ner_tagger(self):
        corenlp_tagger = corenlp.CoreNLPParser(tagtype='ner')

        api_return_value = {
            'sentences': [
                {
                    'index': 0,
                    'tokens': [
                        {
                            'after': ' ',
                            'before': '',
                            'characterOffsetBegin': 0,
                            'characterOffsetEnd': 4,
                            'index': 1,
                            'lemma': 'Rami',
                            'ner': 'PERSON',
                            'originalText': 'Rami',
                            'pos': 'NNP',
                            'word': 'Rami',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 5,
                            'characterOffsetEnd': 8,
                            'index': 2,
                            'lemma': 'Eid',
                            'ner': 'PERSON',
                            'originalText': 'Eid',
                            'pos': 'NNP',
                            'word': 'Eid',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 9,
                            'characterOffsetEnd': 11,
                            'index': 3,
                            'lemma': 'be',
                            'ner': 'O',
                            'originalText': 'is',
                            'pos': 'VBZ',
                            'word': 'is',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 12,
                            'characterOffsetEnd': 20,
                            'index': 4,
                            'lemma': 'study',
                            'ner': 'O',
                            'originalText': 'studying',
                            'pos': 'VBG',
                            'word': 'studying',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 21,
                            'characterOffsetEnd': 23,
                            'index': 5,
                            'lemma': 'at',
                            'ner': 'O',
                            'originalText': 'at',
                            'pos': 'IN',
                            'word': 'at',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 24,
                            'characterOffsetEnd': 29,
                            'index': 6,
                            'lemma': 'Stony',
                            'ner': 'ORGANIZATION',
                            'originalText': 'Stony',
                            'pos': 'NNP',
                            'word': 'Stony',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 30,
                            'characterOffsetEnd': 35,
                            'index': 7,
                            'lemma': 'Brook',
                            'ner': 'ORGANIZATION',
                            'originalText': 'Brook',
                            'pos': 'NNP',
                            'word': 'Brook',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 36,
                            'characterOffsetEnd': 46,
                            'index': 8,
                            'lemma': 'University',
                            'ner': 'ORGANIZATION',
                            'originalText': 'University',
                            'pos': 'NNP',
                            'word': 'University',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 47,
                            'characterOffsetEnd': 49,
                            'index': 9,
                            'lemma': 'in',
                            'ner': 'O',
                            'originalText': 'in',
                            'pos': 'IN',
                            'word': 'in',
                        },
                        {
                            'after': '',
                            'before': ' ',
                            'characterOffsetBegin': 50,
                            'characterOffsetEnd': 52,
                            'index': 10,
                            'lemma': 'NY',
                            'ner': 'O',
                            'originalText': 'NY',
                            'pos': 'NNP',
                            'word': 'NY',
                        },
                    ],
                }
            ]
        }

        corenlp_tagger.api_call = MagicMock(return_value=api_return_value)

        input_tokens = 'Rami Eid is studying at Stony Brook University in NY'.split()
        expected_output = [
            ('Rami', 'PERSON'),
            ('Eid', 'PERSON'),
            ('is', 'O'),
            ('studying', 'O'),
            ('at', 'O'),
            ('Stony', 'ORGANIZATION'),
            ('Brook', 'ORGANIZATION'),
            ('University', 'ORGANIZATION'),
            ('in', 'O'),
            ('NY', 'O'),
        ]
        tagged_output = corenlp_tagger.tag(input_tokens)

        corenlp_tagger.api_call.assert_called_once_with(
            'Rami Eid is studying at Stony Brook University in NY',
            properties={
                'ssplit.isOneSentence': 'true',
                'annotators': 'tokenize,ssplit,ner',
            },
        )
        self.assertEqual(expected_output, tagged_output)

    def test_unexpected_tagtype(self):
        with self.assertRaises(ValueError):
            corenlp_tagger = corenlp.CoreNLPParser(tagtype='test')


class TestParserAPI(TestCase):
    def test_parse(self):
        corenlp_parser = corenlp.CoreNLPParser()

        api_return_value = {
            'sentences': [
                {
                    'basicDependencies': [
                        {
                            'dep': 'ROOT',
                            'dependent': 4,
                            'dependentGloss': 'fox',
                            'governor': 0,
                            'governorGloss': 'ROOT',
                        },
                        {
                            'dep': 'det',
                            'dependent': 1,
                            'dependentGloss': 'The',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 2,
                            'dependentGloss': 'quick',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 3,
                            'dependentGloss': 'brown',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'dep',
                            'dependent': 5,
                            'dependentGloss': 'jumps',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'case',
                            'dependent': 6,
                            'dependentGloss': 'over',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'det',
                            'dependent': 7,
                            'dependentGloss': 'the',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 8,
                            'dependentGloss': 'lazy',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'nmod',
                            'dependent': 9,
                            'dependentGloss': 'dog',
                            'governor': 5,
                            'governorGloss': 'jumps',
                        },
                    ],
                    'enhancedDependencies': [
                        {
                            'dep': 'ROOT',
                            'dependent': 4,
                            'dependentGloss': 'fox',
                            'governor': 0,
                            'governorGloss': 'ROOT',
                        },
                        {
                            'dep': 'det',
                            'dependent': 1,
                            'dependentGloss': 'The',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 2,
                            'dependentGloss': 'quick',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 3,
                            'dependentGloss': 'brown',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'dep',
                            'dependent': 5,
                            'dependentGloss': 'jumps',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'case',
                            'dependent': 6,
                            'dependentGloss': 'over',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'det',
                            'dependent': 7,
                            'dependentGloss': 'the',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 8,
                            'dependentGloss': 'lazy',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'nmod:over',
                            'dependent': 9,
                            'dependentGloss': 'dog',
                            'governor': 5,
                            'governorGloss': 'jumps',
                        },
                    ],
                    'enhancedPlusPlusDependencies': [
                        {
                            'dep': 'ROOT',
                            'dependent': 4,
                            'dependentGloss': 'fox',
                            'governor': 0,
                            'governorGloss': 'ROOT',
                        },
                        {
                            'dep': 'det',
                            'dependent': 1,
                            'dependentGloss': 'The',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 2,
                            'dependentGloss': 'quick',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 3,
                            'dependentGloss': 'brown',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'dep',
                            'dependent': 5,
                            'dependentGloss': 'jumps',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'case',
                            'dependent': 6,
                            'dependentGloss': 'over',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'det',
                            'dependent': 7,
                            'dependentGloss': 'the',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 8,
                            'dependentGloss': 'lazy',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'nmod:over',
                            'dependent': 9,
                            'dependentGloss': 'dog',
                            'governor': 5,
                            'governorGloss': 'jumps',
                        },
                    ],
                    'index': 0,
                    'parse': '(ROOT\n  (NP\n    (NP (DT The) (JJ quick) (JJ brown) (NN fox))\n    (NP\n      (NP (NNS jumps))\n      (PP (IN over)\n        (NP (DT the) (JJ lazy) (NN dog))))))',
                    'tokens': [
                        {
                            'after': ' ',
                            'before': '',
                            'characterOffsetBegin': 0,
                            'characterOffsetEnd': 3,
                            'index': 1,
                            'lemma': 'the',
                            'originalText': 'The',
                            'pos': 'DT',
                            'word': 'The',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 4,
                            'characterOffsetEnd': 9,
                            'index': 2,
                            'lemma': 'quick',
                            'originalText': 'quick',
                            'pos': 'JJ',
                            'word': 'quick',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 10,
                            'characterOffsetEnd': 15,
                            'index': 3,
                            'lemma': 'brown',
                            'originalText': 'brown',
                            'pos': 'JJ',
                            'word': 'brown',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 16,
                            'characterOffsetEnd': 19,
                            'index': 4,
                            'lemma': 'fox',
                            'originalText': 'fox',
                            'pos': 'NN',
                            'word': 'fox',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 20,
                            'characterOffsetEnd': 25,
                            'index': 5,
                            'lemma': 'jump',
                            'originalText': 'jumps',
                            'pos': 'VBZ',
                            'word': 'jumps',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 26,
                            'characterOffsetEnd': 30,
                            'index': 6,
                            'lemma': 'over',
                            'originalText': 'over',
                            'pos': 'IN',
                            'word': 'over',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 31,
                            'characterOffsetEnd': 34,
                            'index': 7,
                            'lemma': 'the',
                            'originalText': 'the',
                            'pos': 'DT',
                            'word': 'the',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 35,
                            'characterOffsetEnd': 39,
                            'index': 8,
                            'lemma': 'lazy',
                            'originalText': 'lazy',
                            'pos': 'JJ',
                            'word': 'lazy',
                        },
                        {
                            'after': '',
                            'before': ' ',
                            'characterOffsetBegin': 40,
                            'characterOffsetEnd': 43,
                            'index': 9,
                            'lemma': 'dog',
                            'originalText': 'dog',
                            'pos': 'NN',
                            'word': 'dog',
                        },
                    ],
                }
            ]
        }

        corenlp_parser.api_call = MagicMock(return_value=api_return_value)

        input_string = "The quick brown fox jumps over the lazy dog".split()
        expected_output = Tree(
            'ROOT',
            [
                Tree(
                    'NP',
                    [
                        Tree(
                            'NP',
                            [
                                Tree('DT', ['The']),
                                Tree('JJ', ['quick']),
                                Tree('JJ', ['brown']),
                                Tree('NN', ['fox']),
                            ],
                        ),
                        Tree(
                            'NP',
                            [
                                Tree('NP', [Tree('NNS', ['jumps'])]),
                                Tree(
                                    'PP',
                                    [
                                        Tree('IN', ['over']),
                                        Tree(
                                            'NP',
                                            [
                                                Tree('DT', ['the']),
                                                Tree('JJ', ['lazy']),
                                                Tree('NN', ['dog']),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ],
        )

        parsed_data = next(corenlp_parser.parse(input_string))

        corenlp_parser.api_call.assert_called_once_with(
            "The quick brown fox jumps over the lazy dog",
            properties={'ssplit.eolonly': 'true'},
        )
        self.assertEqual(expected_output, parsed_data)

    def test_dependency_parser(self):
        corenlp_parser = corenlp.CoreNLPDependencyParser()

        api_return_value = {
            'sentences': [
                {
                    'basicDependencies': [
                        {
                            'dep': 'ROOT',
                            'dependent': 5,
                            'dependentGloss': 'jumps',
                            'governor': 0,
                            'governorGloss': 'ROOT',
                        },
                        {
                            'dep': 'det',
                            'dependent': 1,
                            'dependentGloss': 'The',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 2,
                            'dependentGloss': 'quick',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 3,
                            'dependentGloss': 'brown',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'nsubj',
                            'dependent': 4,
                            'dependentGloss': 'fox',
                            'governor': 5,
                            'governorGloss': 'jumps',
                        },
                        {
                            'dep': 'case',
                            'dependent': 6,
                            'dependentGloss': 'over',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'det',
                            'dependent': 7,
                            'dependentGloss': 'the',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 8,
                            'dependentGloss': 'lazy',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'nmod',
                            'dependent': 9,
                            'dependentGloss': 'dog',
                            'governor': 5,
                            'governorGloss': 'jumps',
                        },
                    ],
                    'enhancedDependencies': [
                        {
                            'dep': 'ROOT',
                            'dependent': 5,
                            'dependentGloss': 'jumps',
                            'governor': 0,
                            'governorGloss': 'ROOT',
                        },
                        {
                            'dep': 'det',
                            'dependent': 1,
                            'dependentGloss': 'The',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 2,
                            'dependentGloss': 'quick',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 3,
                            'dependentGloss': 'brown',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'nsubj',
                            'dependent': 4,
                            'dependentGloss': 'fox',
                            'governor': 5,
                            'governorGloss': 'jumps',
                        },
                        {
                            'dep': 'case',
                            'dependent': 6,
                            'dependentGloss': 'over',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'det',
                            'dependent': 7,
                            'dependentGloss': 'the',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 8,
                            'dependentGloss': 'lazy',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'nmod:over',
                            'dependent': 9,
                            'dependentGloss': 'dog',
                            'governor': 5,
                            'governorGloss': 'jumps',
                        },
                    ],
                    'enhancedPlusPlusDependencies': [
                        {
                            'dep': 'ROOT',
                            'dependent': 5,
                            'dependentGloss': 'jumps',
                            'governor': 0,
                            'governorGloss': 'ROOT',
                        },
                        {
                            'dep': 'det',
                            'dependent': 1,
                            'dependentGloss': 'The',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 2,
                            'dependentGloss': 'quick',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 3,
                            'dependentGloss': 'brown',
                            'governor': 4,
                            'governorGloss': 'fox',
                        },
                        {
                            'dep': 'nsubj',
                            'dependent': 4,
                            'dependentGloss': 'fox',
                            'governor': 5,
                            'governorGloss': 'jumps',
                        },
                        {
                            'dep': 'case',
                            'dependent': 6,
                            'dependentGloss': 'over',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'det',
                            'dependent': 7,
                            'dependentGloss': 'the',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'amod',
                            'dependent': 8,
                            'dependentGloss': 'lazy',
                            'governor': 9,
                            'governorGloss': 'dog',
                        },
                        {
                            'dep': 'nmod:over',
                            'dependent': 9,
                            'dependentGloss': 'dog',
                            'governor': 5,
                            'governorGloss': 'jumps',
                        },
                    ],
                    'index': 0,
                    'tokens': [
                        {
                            'after': ' ',
                            'before': '',
                            'characterOffsetBegin': 0,
                            'characterOffsetEnd': 3,
                            'index': 1,
                            'lemma': 'the',
                            'originalText': 'The',
                            'pos': 'DT',
                            'word': 'The',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 4,
                            'characterOffsetEnd': 9,
                            'index': 2,
                            'lemma': 'quick',
                            'originalText': 'quick',
                            'pos': 'JJ',
                            'word': 'quick',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 10,
                            'characterOffsetEnd': 15,
                            'index': 3,
                            'lemma': 'brown',
                            'originalText': 'brown',
                            'pos': 'JJ',
                            'word': 'brown',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 16,
                            'characterOffsetEnd': 19,
                            'index': 4,
                            'lemma': 'fox',
                            'originalText': 'fox',
                            'pos': 'NN',
                            'word': 'fox',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 20,
                            'characterOffsetEnd': 25,
                            'index': 5,
                            'lemma': 'jump',
                            'originalText': 'jumps',
                            'pos': 'VBZ',
                            'word': 'jumps',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 26,
                            'characterOffsetEnd': 30,
                            'index': 6,
                            'lemma': 'over',
                            'originalText': 'over',
                            'pos': 'IN',
                            'word': 'over',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 31,
                            'characterOffsetEnd': 34,
                            'index': 7,
                            'lemma': 'the',
                            'originalText': 'the',
                            'pos': 'DT',
                            'word': 'the',
                        },
                        {
                            'after': ' ',
                            'before': ' ',
                            'characterOffsetBegin': 35,
                            'characterOffsetEnd': 39,
                            'index': 8,
                            'lemma': 'lazy',
                            'originalText': 'lazy',
                            'pos': 'JJ',
                            'word': 'lazy',
                        },
                        {
                            'after': '',
                            'before': ' ',
                            'characterOffsetBegin': 40,
                            'characterOffsetEnd': 43,
                            'index': 9,
                            'lemma': 'dog',
                            'originalText': 'dog',
                            'pos': 'NN',
                            'word': 'dog',
                        },
                    ],
                }
            ]
        }

        corenlp_parser.api_call = MagicMock(return_value=api_return_value)

        input_string = "The quick brown fox jumps over the lazy dog".split()
        expected_output = Tree(
            'jumps',
            [
                Tree('fox', ['The', 'quick', 'brown']),
                Tree('dog', ['over', 'the', 'lazy']),
            ],
        )

        parsed_data = next(corenlp_parser.parse(input_string))

        corenlp_parser.api_call.assert_called_once_with(
            "The quick brown fox jumps over the lazy dog",
            properties={'ssplit.eolonly': 'true'},
        )
        self.assertEqual(expected_output, parsed_data.tree())
