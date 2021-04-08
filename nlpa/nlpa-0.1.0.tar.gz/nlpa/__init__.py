import pandas as pd
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import emoji
import string
import re
import contractions


__version__ = "0.1.0"  # Version of the Package
__author__ = 'Anup Prakash'  # Author of the Package


class CleanText:  # CleanText -> name of the Class and all the Functionality Starts here

    """
    This Class Integrate some of the Functionality of the Natural Language Tooltik(NLTK).
    The purpose of this Library is to automate the task which generally repeated mostly all the time,
    during the cleansing of the Text Data.

    So, here we can do all the cleansing with a simple call of the functions.

    Attributes
    ----------
    self.vals : pandas.Series
        Pandas Series is a one-dimensional labeled array capable of holding data of any type (integer, string, float, python objects, etc.). 

    Methods
    -------
        lower_text(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype())
            This method take a pandas Series as Input and lower the text

        remove_contraction_map(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype())
            This method take a pandas Series as Input and remove the Contraction map from the Text

        remove_punctuation(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype())
            This method take a pandas Series as Input and remove the punctuation marks from the Text

        remove_numbers(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype())
            This method take a pandas Series as Input and remove the Numbers from the Text

        remove_url(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype())
            This method take a pandas Series as Input and remove the URL from the Text
        
        remove_social_tags(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype())
            This method take a pandas Series as Input and remove the Social Media Tags from the Text
        
        remove_emojis(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype()):
            This method take a pandas Series as Input and remove the Emojis from the Text
        
        word_tokenize(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype())
            This method take a pandas Series as Input and Tokenize the Word
        
        remove_stopwords(self, vals=pd.Series([], dtype=pd.StringDtype()), tokenized=False, lang='english') -> pd.Series([], dtype=pd.StringDtype())
            This method take a pandas Series as Input and Remove the stopword(words which are very frequently used)
        
        word_lemmatize(self, vals=pd.Series([], dtype=pd.StringDtype()), tokenize=False) -> pd.Series([], dtype=pd.StringDtype())
            This method take a pandas Series as Input and Lemmatize the word(Bring the word to its root form)

        cleanData(self) -> pd.Series([], dtype=pd.StringDtype())
            This method take a pandas Series as Input from the class(not from the Parameters)
    """

    def __init__(self, vals=pd.Series([], dtype=pd.StringDtype())):
        """
        Constructor Take input of Pandas Series and delete the NaN value if present
        """
        self.vals = vals
        self.vals.dropna(inplace=True)

    # ----------------------------- Lowering Alphabets -----------------------------------------
    def lower_text(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype()):
        """
        This method take a pandas Series as Input and 
        lower the text 
        Example - > 
        Input Text = we're the BEST MUSIC
        Output Text = we're the best Music

        and the same text is  returned in  Pandas Series Format.

        Parameters
        ----------
            vals : pandas.Series()
                The text on which text to be perform

        Returns
        -------
            pandas.Series()
                a pandas series 

        If no parameter is provided then it take value, which was defined in the constructor 
        self.vals
        """
        if (vals.empty):
            vals = self.vals
        return vals.str.lower()

    # ----------------------------- Removing Social Media Slangs -----------------------------------------
    # def remove_social_slangs(self, vals=pd.Series([], dtype=pd.StringDtype())):
    #     if (vals.empty):
    #         vals = self.vals

    #     return vals.apply(lambda raw: ' '.join([slangs[clean] if clean in slangs else clean for clean in raw.split()]))

    # ----------------------------- Correcting Contraction Map -----------------------------------------
    # we're = we are
    def remove_contraction_map(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype()):
        """
        This method take a pandas Series as Input and 

        remove the Contraction map from the Text
        Example - > 
        Input Text = we're the best Music 
        Output Text = we are the best Music

        and the same text is  returned in  Pandas Series Format.

        Parameters
        ----------
            vals : pandas.Series()
                The text on which text to be perform

        Returns
        -------
            pandas.Series()
                a pandas series 

        If no parameter is provided then it take value, which was defined in the constructor 
        self.vals
        """
        if (vals.empty):
            vals = self.vals

        return vals.dropna().apply(lambda raw: ''.join([contractions.fix(raw)]))

    # ----------------------------- Removing Punctuations -----------------------------------------
    def remove_punctuation(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype()):
        """
        This method take a pandas Series as Input and 

        remove the punctuation marks  from the Text
        Example - > 
        Input Text = we are the best Music....!
        Output Text = we are the best Music

        and the same text is  returned in  Pandas Series Format.

        Parameters
        ----------
            vals : pandas.Series()
                The text on which text to be perform

        Returns
        -------
            pandas.Series()
                a pandas series 

        If no parameter is provided then it take value, which was defined in the constructor 
        self.vals
        """
        if (vals.empty):
            vals = self.vals

        return vals.dropna().apply(lambda raw: ''.join([clean for clean in raw if clean not in string.punctuation]))

    # ----------------------------- Removing Number From Passage -----------------------------------------
    def remove_numbers(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype()):
        """
        This method take a pandas Series as Input and 

        remove the Numbers from the Text
        Example - > 
        Input Text = we are the best Music123444
        Output Text = we are the best Music

        and the same text is  returned in  Pandas Series Format.

        Parameters
        ----------
            vals : pandas.Series()
                The text on which text to be perform

        Returns
        -------
            pandas.Series()
                a pandas series 

        If no parameter is provided then it take value, which was defined in the constructor 
        self.vals
        """
        if (vals.empty):
            vals = self.vals

        return vals.dropna().apply(lambda raw: ''.join([clean for clean in raw if not clean.isdigit()]))

    # ----------------------------- Removing URLS -----------------------------------------
    def remove_url(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype()):
        """
        This method take a pandas Series as Input and 

        remove the URL from the Text
        Example - > 
        Input Text = we are the best Music for more https://www.xyz.com
        Output Text = we are the best Music

        and the same text is  returned in  Pandas Series Format.

        Parameters
        ----------
            vals : pandas.Series()
                The text on which text to be perform

        Returns
        -------
            pandas.Series()
                a pandas series 

        If no parameter is provided then it take value, which was defined in the constructor 
        self.vals
        """
        if (vals.empty):
            vals = self.vals

        return vals.dropna().apply(lambda raw: ''.join([re.sub(r"http\S+", "", raw)]))

    # ----------------------------- Removing Social Media Tags (# and @) -----------------------------------------
    def remove_social_tags(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype()):
        """
        This method take a pandas Series as Input and 

        remove the Social Media Tags  from the Text
        Example - > 
        Input Text = we are the best @Music #newsongs
        Output Text = we are the best newsongs

        and the same text is  returned in  Pandas Series Format.

        Parameters
        ----------
            vals : pandas.Series()
                The text on which text to be perform

        Returns
        -------
            pandas.Series()
                a pandas series 

        If no parameter is provided then it take value, which was defined in the constructor 
        self.vals
        """
        if (vals.empty):
            vals = self.vals

        return vals.dropna().apply(lambda raw: ''.join([re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", raw)]))

    # ----------------------------- Removing Emojis -----------------------------------------
    def remove_emojis(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype()):
        """
        This method take a pandas Series as Input and 

        remove the Emojis from the Text
        Example - > 
        Input Text = we are the best :) Music....!
        Output Text = we are the best Music

        and the same text is  returned in  Pandas Series Format.

        Parameters
        ----------
            vals : pandas.Series()
                The text on which text to be perform

        Returns
        -------
            pandas.Series()
                a pandas series 

        If no parameter is provided then it take value, which was defined in the constructor 
        self.vals
        """
        if (vals.empty):
            vals = self.vals

        return vals.dropna().apply(lambda raw: ''.join([clean for clean in raw if clean not in emoji.UNICODE_EMOJI]))

    # ----------------------------- Tokenizing Words -----------------------------------------
    def word_tokenize(self, vals=pd.Series([], dtype=pd.StringDtype())) -> pd.Series([], dtype=pd.StringDtype()):
        """
        This method take a pandas Series as Input and 

        Tokenize the Word 
        Example - > 
        Input Text = we are the best Music
        Output Text = ['we','are', 'the', 'best', 'Music']

        and the same text is  returned in  Pandas Series Format.

        Parameters
        ----------
            vals : pandas.Series()
                The text on which text to be perform

        Returns
        -------
            pandas.Series()
                a pandas series 

        If no parameter is provided then it take value, which was defined in the constructor 
        self.vals
        """
        if (vals.empty):
            vals = self.vals

        return vals.apply(lambda words: word_tokenize(words))

    # ----------------------------- Removing Stop Words -----------------------------------------
    def remove_stopwords(self, vals=pd.Series([], dtype=pd.StringDtype()), tokenized=False, lang='english') -> pd.Series([], dtype=pd.StringDtype()):
        """
        This method take a pandas Series as Input and 

        Remove the stopword (words which are very frequently used)
        Example - > 
        Input Text = we are the best Music
        Output Text = best Music

        and the same text is  returned in  Pandas Series Format.

        Parameters
        ----------
            vals : pandas.Series()
                The text on which text to be perform
            tokenized : boolean
                the input value is tokeinized or not
            lang : string
                of which language you want to remove the stopwords

        Returns
        -------
            pandas.Series()
                a pandas series 

        If no parameter is provided then it take value, which was defined in the constructor 
        self.vals
        """
        if (vals.empty):
            vals = self.vals
        if not tokenized:
            vals = self.word_tokenize(vals)
            return vals.apply(lambda raw: ' '.join([clean for clean in raw if clean not in stopwords.words(lang)]))

        return vals.apply(lambda raw: ' '.join([clean for clean in raw if clean not in stopwords.words(lang)]))

    # ----------------------------- Part of Speech Tagging -----------------------------------------
    def get_wordnet_pos(self, pos_tag):
        tag_map = {
            'CC': None,  # coordin. conjunction (and, but, or)
            'CD': wn.NOUN,  # cardinal number (one, two)
            'DT': None,  # determiner (a, the)
            'EX': wn.ADV,  # existential ‘there’ (there)
            'FW': None,  # foreign word (mea culpa)
            'IN': wn.ADV,  # preposition/sub-conj (of, in, by)
            'JJ': wn.ADJ,  # adjective (yellow)
            'JJR': wn.ADJ,  # adj., comparative (bigger)
            'JJS': wn.ADJ,  # adj., superlative (wildest)
            'LS': None,  # list item marker (1, 2, One)
            'MD': None,  # modal (can, should)
            'NN': wn.NOUN,  # noun, sing. or mass (llama)
            'NNS': wn.NOUN,  # noun, plural (llamas)
            'NNP': wn.NOUN,  # proper noun, sing. (IBM)
            'NNPS': wn.NOUN,  # proper noun, plural (Carolinas)
            'PDT': wn.ADJ,  # predeterminer (all, both)
            'POS': None,  # possessive ending (’s )
            'PRP': None,  # personal pronoun (I, you, he)
            'PRP$': None,  # possessive pronoun (your, one’s)
            'RB': wn.ADV,  # adverb (quickly, never)
            'RBR': wn.ADV,  # adverb, comparative (faster)
            'RBS': wn.ADV,  # adverb, superlative (fastest)
            'RP': wn.ADJ,  # particle (up, off)
            'SYM': None,  # symbol (+,%, &)
            'TO': None,  # “to” (to)
            'UH': None,  # interjection (ah, oops)
            'VB': wn.VERB,  # verb base form (eat)
            'VBD': wn.VERB,  # verb past tense (ate)
            'VBG': wn.VERB,  # verb gerund (eating)
            'VBN': wn.VERB,  # verb past participle (eaten)
            'VBP': wn.VERB,  # verb non-3sg pres (eat)
            'VBZ': wn.VERB,  # verb 3sg pres (eats)
            'WDT': None,  # wh-determiner (which, that)
            'WP': None,  # wh-pronoun (what, who)
            'WP$': None,  # possessive (wh- whose)
            'WRB': None,  # wh-adverb (how, where)
            '$': None,  # dollar sign ($)
            '#': None,  # pound sign (#)
            '“': None,  # left quote (‘ or “)
            '”': None,  # right quote (’ or ”)
            '(': None,  # left parenthesis ([, (, {, <)
            ')': None,  # right parenthesis (], ), }, >)
            ',': None,  # comma (,)
            '.': None,  # sentence-final punc (. ! ?)
            ':': None,  # mid-sentence punc (: ; ... – -)
            '\'': None,
            "''": None
        }
        return tag_map[pos_tag] if (tag_map[pos_tag]) else wn.NOUN

    # ----------------------------- Word Lemmatize (Root Words) -----------------------------------------
    def word_lemmatize(self, vals=pd.Series([], dtype=pd.StringDtype()), tokenize=False) -> pd.Series([], dtype=pd.StringDtype()):
        """
        This method take a pandas Series as Input and 

        Lemmatize the word (Bring the word to its root form)
        Example - > 
        Input Text = walking on new road
        Output Text = walk on new road

        and the same text is  returned in  Pandas Series Format.

        Parameters
        ----------
            vals : pandas.Series()
                The text on which text to be perform
            tokenize : boolean
                the input value is tokeinized or not
            

        Returns
        -------
            pandas.Series()
                a pandas series 

        If no parameter is provided then it take value, which was defined in the constructor 
        self.vals
        """
        if (vals.empty):
            vals = self.vals

        if(not tokenize):
            vals = self.word_tokenize(vals)
            vals = vals.apply(lambda x: pos_tag(x))
            return vals.apply(lambda raw: ' '.join([WordNetLemmatizer().lemmatize(words, self.get_wordnet_pos(raw_pos)) for words, raw_pos in raw]))

        vals = vals.apply(lambda x: pos_tag(x))
        return vals.apply(lambda raw: ' '.join([WordNetLemmatizer().lemmatize(words, self.get_wordnet_pos(raw_pos)) for words, raw_pos in raw]))

    def cleanData(self) -> pd.Series([], dtype=pd.StringDtype()):
        """
        This method take a pandas Series as Input from the class(not from the Parameters) and 

        this function 
        1-> Lower the text
        2-> Remove Contraction Map
        3-> Remove Url
        4-> Remove Social Tags
        5-> Remove Emojis
        6-> Remove Punctuation
        7-> Word Tokenize
        8-> Remove Stopwords
        9-> Word_lemmatize
        (output of each function is input for the next functions)

        Example - > 
        Input Text = we are the best Music
        Output Text = best Music

        and the same text is  returned in  Pandas Series Format.

        If no parameter is provided then it take value, which was defined in the constructor 
        self.vals
        """
        return self.word_lemmatize(self.remove_stopwords(self.word_tokenize(self.remove_punctuation(self.remove_emojis(self.remove_social_tags(self.remove_url(self.remove_contraction_map(self.lower_text())))))), tokenized=True))
