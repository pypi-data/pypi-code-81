r"""NLP Library Toolkit
Created by Juan Camilo Díaz just for fun.
"""

__version__ = '0.0.1'
__author__ = 'Juan Camilo Diaz <juancadh@gmail.com>'
# __all__ = [
#     'testme', 'load_json_file', 'write_json_file'
# ]

import re
import sys
import os
import json
import nltk
import random
import string
import pickle
import warnings
import numpy as np
import pandas as pd
from tqdm import tqdm
from time import time
from bs4 import BeautifulSoup
from emoji import UNICODE_EMOJI
from nltk.corpus import stopwords
from matplotlib import pyplot as plt
from sklearn.ensemble import VotingClassifier
from sklearn.naive_bayes import MultinomialNB
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from nltk.tokenize import word_tokenize, sent_tokenize, line_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV, SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, recall_score, precision_score

# import torch
# import torch.nn.functional as F
# from torch.autograd import Variable

def warn(*args, **kwargs):
    pass
warnings.warn = warn

THIS_PATH  = os.path.dirname(os.path.abspath(__file__))

# ============================================================================================================== 
def testme():
    print("I'm working dude!")

# ============================================================================================================== 
def load_json_file(file):
    """Load .json file.
    Parameters
    --------------
    - file: String
        Json file path.
        Example: ./mydata/myfile.json
    """
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# ============================================================================================================== 
def write_json_file(file, data, indent=4):
    """Write data into .json file. It rewrites the entire document. 
    Parameters
    --------------
    - file: String
        Json file path.
        Example: ./mydata/myfile.json
    - data: list of dictionary
        Data that want to be saved in file
        Example: [1,3,4,5] or {'name':'juan', 'accounts':['google', 'facebook']}
    - indent: integer
        Indentation of json file. None is the most compact representation.
    """
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)
        print(f"File {file} was correctly written.")

# ==============================================================================================================

def _tag_person(ner):
    """Function that creates the @sys-person entity tag in pre-tagged text with @sys-name and @sys-lastname tags.
    Parameters
    -----------

    - ner: Object
        Object that returns the function ner_rule_based_sp()
    """

    text_original = ner['text']
    sentence = ner['text_tagged']
    original_patterns = ner['patterns']

    words = sentence.split(" ")
    # words = word_tokenize(sentence)

    nametags =["@sys-name", "@sys-lastname"]
    recreate_w = []
    match = False

    # Take only the patterns that matter
    filtered_patterns = []
    for entity in original_patterns:
        if entity['tag'] in nametags:
            filtered_patterns.append(entity)

    first_pos_match = 0
    last_pos_match = 0
    first_person_pos_match = -1
    last_person_pos_match = -1
    first_position_original = -1
    last_position_original = -1
    space_counter = 0
    tags_person = []
    tag_position_in_patterns = 0

    for i in range(len(words)):
        # Current Position (length + whitespace)
        if i == 0:
            last_pos_match += len(words[i]) - 1
        else:
            last_pos_match += len(words[i]) + 1
        
        first_pos_match = last_pos_match - len(words[i]) + 1
        # print(first_pos_match, last_pos_match)

        # Match the posterior occurance of name or lastname
        if words[i] in nametags and match:
            last_person_pos_match = last_pos_match
            last_position_original = filtered_patterns[tag_position_in_patterns]['position'][1]
            tag_position_in_patterns += 1

        # Match the first occurance of name or lastname
        if words[i] in nametags and not match:
            match = True
            recreate_w.append("@sys-person")
            first_person_pos_match = first_pos_match
            first_position_original = filtered_patterns[tag_position_in_patterns]['position'][0]
            last_position_original = filtered_patterns[tag_position_in_patterns]['position'][1]
            tag_position_in_patterns += 1

        # Match anything that is not name or lastname
        if words[i] not in nametags or i == len(words):
            if match:
                # print(f"tag postion: {first_person_pos_match} - {last_person_pos_match}")
                # print(f"tag postion in original: {first_position_original} - {last_position_original}")
                original_patterns.append({
                    'match': text_original[first_position_original:last_position_original+1], 
                    'position': (first_position_original, last_position_original), 
                    'tag': '@sys-person', 
                    'entity': 'Nombre y/o apellido de persona'
                })
                
            recreate_w.append(words[i])
            match = False
            first_person_pos_match = -1
            last_person_pos_match = -1

    # Recreate new text with sys-person tag
    new_text_tagged = ' '.join(recreate_w)
    # new_text_tagged = TreebankWordDetokenizer().detokenize(recreate_w))
    
    # Remove duplicates in patterns
    new_patterns = [dict(t) for t in {tuple(d.items()) for d in original_patterns}]
    # Sort the pattersn by first span position
    new_patterns = sorted(new_patterns, key=lambda x: x['position'][0], reverse=False)

    results = {
        'text' : text_original,
        'text_tagged' : new_text_tagged,
        'patterns' : new_patterns
    }

    return results

def ner_rule_based_sp(text, tags=[], not_tags=[], other_regexp = [], other_entities = []):
    """Extract spanish entities from text using Rule-Base Method.
    Important
    ---------------
    The file nlp_jcd_entities.json must exist in the same route of this file in order to exist.
    
    Parameters
    ---------------
    - text: String
        Text from which is needed to extract entities.
        Example: "Mi nombre es Juan Camilo mi correo es jc@me.com."
    - tags: list
        List of tags that want to be searched. If empty then all entitites are included.        
        Example: ["@sys-name", "@sys-lastname", "@sys-date", "@sys-num-positiveinteger", "@sys-typeid", ...]
    - not_tags: list
        List of tags that dont want to be included in search.
         Example:  ["@sys-num-any"]

    Note
    -----------
    List of possible tags:
    "@sys-email", "@sys-num-any", "@sys-num-signedinteger", "@sys-num-positiveinteger", "@sys-num-positivedecimal", "@sys-num-signeddecimal", "@sys-percentage", "@sys-currency", "@sys-date", "@sys-time", 
    "@sys-name", "@sys-lastname", "@sys-dayofweek", "@sys-monthofyear", "@sys-country", "@sys-cardinalpoint", "@sys-color", "@sys-units-name", "@sys-units-symbol", "@sys-multiplier-name", "@sys-submultiplier-name", "@sys-gender", "@sys-race", "@sys-typeid"
    """
    
    # Open the file
    f = open(f'{THIS_PATH}/nlp_jcd_entities.json',)
    data_entities = json.load(f)
    f.close()

    entities_dic = {}
    reMatches = []
    tagged_text = text

    entities_regex = data_entities['entities_regex']
    entities = data_entities['entities']
    
    original_tags = [x for x in tags]
    original_notags = [x for x in not_tags]

    # If no tags selected the append them all
    if len(tags) == 0:
        for entity in entities_regex:
            tags.append(entity['id'])
        for entity in entities:
            tags.append(entity['id'])
            tags.append("@sys-person")
        original_tags = tags

    if "@sys-person" in tags and '@sys-name' not in tags:
        tags.append('@sys-name')

    if "@sys-person" in tags and '@sys-lastname' not in tags:
        tags.append('@sys-lastname')

    if "@sys-person" in tags and '@sys-name' in not_tags:
        not_tags.remove('@sys-name')
    
    if "@sys-person" in tags and '@sys-lastname' in not_tags:
        not_tags.remove('@sys-lastname')

    try:
        # Search all regex entity tags    
        for regexEntity in entities_regex:
            for theRegex in regexEntity['regex']:
                entityName = regexEntity['name']
                entityTag = regexEntity['id']        
                if entityTag in tags and entityTag not in not_tags:
                    for x in re.finditer(theRegex, text):
                        reMatches.append({'match': x.group(), 'position': x.span(), 'tag':entityTag, 'entity':entityName } )
    except Exception as e:
        print(f"There was an error extracting entities. Regular Expressions. Error: {str(e)}")

    # Search entities by pre-defined classification. Must be the entire word. TODO: Handle things like 100Kg, 200g
    try:
        # Tokenize original sentence
        tokens_org = word_tokenize(text)        
        # Tokenize the sentence and remove accents and lowecase it
        nlpt = nlp_tools('spanish')
        trans_text = nlpt.preprocess_text(text, remove_accents=True)
        tokens = word_tokenize(trans_text)
        # Dictionary of correspondences
        tokenstrans_dic = dict(zip(tokens,tokens_org))

        for entity in entities:
            entityName = entity['name']
            entityTag = entity['id']
            entityData = entity['data']
            if entityTag in tags and entityTag not in not_tags:
                for tagEntity in entityData:
                    if entityTag == "@sys-name" or entityTag == "@sys-lastname":                        
                        if len(tagEntity) > 3:
                            tagEntity = nlpt.preprocess_text(tagEntity, remove_accents=True)     
                    else:
                        tagEntity = nlpt.preprocess_text(tagEntity, remove_accents=True)     

                    for x in re.finditer(rf'\b{tagEntity}\b', trans_text):
                        #' '.join([tokenstrans_dic[t] for t in word_tokenize(x.group())])
                        match = text[x.span()[0]:x.span()[1]]
                        reMatches.append({'match': match, 'position': (x.span()[0], x.span()[1]-1), 'tag':entityTag, 'entity':entityName } )

    except Exception as e:
        print(f"There was an error extracting entities. From pre-defined lists. Error: {str(e)}")

    # Replace original text with entity tags
    try:
        tagged_text = text
        for reEntity in reMatches:
            # El orden de los tags en el archivo nlp_jcd_entities.json es muy importtante!! 
            # El tag de numero (@sys-num-any) debe estar de ultimo para que por ejmeplo primerdo identifique fechas y luego si numeros.
            tagged_text = re.sub(rf"\b{reEntity['match']}\b", reEntity['tag'], tagged_text)
    except Exception:
        print("There was an error replacing tags in entites.")

    # Remove duplicates in patterns
    reMatches = [dict(t) for t in {tuple(d.items()) for d in reMatches}]
    # Sort the pattersn by first span position
    patterns = sorted(reMatches, key=lambda x: x['position'][0], reverse=False)

    entities_dic = {
        'text' : text,
        'text_tagged' : tagged_text,
        'patterns' : patterns
    }

    # Search for @sys-person tags
    
    if "@sys-person" in tags and "@sys-person" not in not_tags:
        entities_dic = _tag_person(entities_dic)

        # Filter if name or last name are not intended to retrieve                
        filtered_entities = []
        for entity in entities_dic['patterns']:
            if entity['tag'] == "@sys-name" and ("@sys-name" not in original_tags or "@sys-name" in original_notags):
                continue
            if entity['tag'] == "@sys-lastname" and ("@sys-lastname" not in original_tags or "@sys-lastname" in original_notags):
                continue
    
            filtered_entities.append(entity)

        entities_dic = {
            'text' : entities_dic['text'],
            'text_tagged' : entities_dic['text_tagged'],
            'patterns' : filtered_entities
        }

    return entities_dic


# ==============================================================================================================
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[97m'
    LIGHTGRAY = '\033[37m'
    CYAN = '\033[36m'

# ==============================================================================================================
class nlp_tools():
    """ Text Mining toolkits
    Methods
    -------------
    1. top_ngram(corpus, n_gram): Count the number of words by n-gram. Frequency of 2 words, 3 words, ....
    2. plural_word(list_of_words): Converts a list of words in its plural form.
    3. emojis_freq(text): Returns the sorted list of most frequently used emojis in a text.
    4. number_of_emojies(text): Counts the number of emojies in a text.
    5. count_chars(text): Function that count the number of characters in a text excluding spaces.
    6. perc_puntuation(text): Function that compute the percentage of puntation of a text.

    Example:
    txt_tool = nlp_tools(lang = 'spanish')    
    """
    def __init__(self, lang = 'english'):
        self.lang = lang

    def preprocess_text(self, text, lowercase = True, rem_stopwords = False, lemmatize = False, remove_accents = False, remove_html = False, remove_punctuation = False, domain_sp_stopwrd = [], regex_sub = []):
        """ Preprocess a specific text.
        Parameters
        --------------
        - lowercase: Boolean
            True if want to convert text to lowercase
        - rem_stopword: Boolean
            True if want to remove stopwords
        - lemmatize: Boolean
            True if want to lemmatize
        - remove_html: Boolean
            True if want to remove HTML tags/language
        - remove_punctuation  : Boolean
            True if want to remove puntuation !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        - remove_accents: Boolean
            True if want to remove accents in text
        - domain_sp_stopwrd : List
            List of domain specific stopwords to remove. Ex: ['X1', 'YX2', ...] 
        - regex_sub : List
            List of regular expresions to remove. Ex: ['[^a-zA-Z]']

        Returns
        -------
        - string
            Text pre-processed

        Example
        ------------
        txt_data = "Hola, Soy Juan Camilo esto es una prueba de lo un texto que NecEsiista ser pre-processado!"
        clean_txt = preprocess_text(
            txt_data
            , lowercase= True
            , rem_stopwords= True
            , lemmatize= False
            , remove_html = True
            , remove_punctuation = True
            , domain_sp_stopwrd=['media','omitted','missed','voice','call']
            , regex_sub=['ja+']
        )
        """

        # Make sure it is string
        text = str(text)

        # Remove white spaces in text
        text = text.strip()

        # Lowercase text
        if lowercase:
            text = text.lower()
        
        # Remove RegExs
        if len(regex_sub) > 0:
            for rg in regex_sub:
                text = re.sub(rg, '', text)

        # Remove HTML
        if remove_html:
            text = BeautifulSoup(text).get_text()

        # Replace special accents
        if remove_accents:
            replacements = (("[àáâãäå]", "a"), ("[èéêë]", "e"), ("[ìíîï]", "i"), ("[òóôõö]", "o"), ("[ùúûü]", "u"))
            if self.lang == "spanish" or self.lang == "english":
                for a, b in replacements:
                    text = re.sub(rf"{a}", b, text)

        # Remove punctuation in sentence
        if remove_punctuation:
            punctuation = '!"#$%&\'()*+,-./:;<=>?[\\]^_`{|}~\“\”\¡\¿\«\»\…\—\−'
            text = re.sub(rf'(?!\b[^\w\s]\b)[{punctuation}]', '', text)

        # Remove domain specific stopwords
        if len(domain_sp_stopwrd) > 0:
            for dst in domain_sp_stopwrd:
                r = dst.lower()
                text = re.sub(rf"\b{r}\b", '', text.lower())
        
        # Remove stopwords
        stop_words = set(stopwords.words(self.lang))
        if rem_stopwords:
            word_tokens = word_tokenize(text)
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            text = ' '.join(filtered_sentence)

        # Lematize, only in english
        if lemmatize:
            if self.lang == 'english':
                text = text.split()
                lem = WordNetLemmatizer()
                text = [lem.lemmatize(w) for w in text if not w in stop_words] 
                text = ' '.join(text)
            else:
                print("Lemmatization only works with English language")

        return text

    def tokenize_text(self, text, type_="word"):
        """ Function used for tokenization. 
        Parameters 
        ------------        
        - text: Text to be tokenized as string. 
        - type_: Type of tokenization:
            * word (split by words and punctuation)
            * word-simple (split just by spaces, doesn't consider punctuation)
            * letter (split by letters and punctuation)
            * sentence (split by sentences)
            * line (split by line breaks)

        Example
        ----------

        text = "Hola!, Como estas?. Mi nombre es Juan. \n Gracias por venir!"
        tokenize_text(text)
        tokenize_text(text, "sentence")
        """
        if type_ == "word":
            return word_tokenize(text)
        elif type_ == "word-simple":
            return text.split(" ")
        elif type_ == "letter":
            return [x.split() for x in text]
        elif type_ == "sentence":
            return sent_tokenize(text)
        elif type_ == "sentence":
            return sent_tokenize(text)
        else:
            return word_tokenize(text)
        
    def top_ngram(self, corpus, n_gram):
        """ Count the number of words by n-gram. Frequency of 2 words, 3 words, ....
            - Corpus : List of values with the text to be analyzed Ex: ["Hi Im Juan", "Hello, Im Maria", "Nice to meet you"]
            - n_gram : Number of words.
        """

        vec = CountVectorizer(ngram_range=(n_gram, n_gram), max_features=2000).fit(corpus)
        bag_of_words = vec.transform(corpus)
            
        sum_words = bag_of_words.sum(axis=0) 

        words_freq = []
        for word, idx in vec.vocabulary_.items():
            words_freq.append((word, sum_words[0, idx]))
            
        words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
        top_df = pd.DataFrame(words_freq)
        top_df.columns = ["Ngram", "Frequency"]
        return top_df
        
    def plural_word(self, list_of_words):
        """ Function that converts a list of words in its plural form"""

        if self.lang == 'spanish':
            plurals = []
            grp_1 = ["í","ó","ú","á","d","l","r","n","b","c","y","j"]
            grp_2 = ["a","e","i","o","u","é",]
            grp_3 = ["s", "x"]
            for word in ls_wds:
                wd     = word.lower()
                last_1 = wd[-1]
                if last_1 == "z":
                    root_wd = wd[:len(wd)-1]
                    plural  = root_wd + "ces"
                elif last_1 in grp_1:
                    root_wd = wd
                    plural  = root_wd + "es"
                elif last_1 in grp_2:
                    root_wd = wd
                    plural  = root_wd + "s"
                elif last_1 in grp_3:
                    root_wd = wd
                    plural  = root_wd
                else:
                    root_wd = wd
                    plural  = root_wd + "s"

                plurals.append(plural)

            return plurals
        else:
            print("(!) Language not supported")
            return []

    def emojis_freq(sefl, text):
        """ Return the sorted list of most frequently used emojis in a text"""
        df_emojis = [i for i in text if i in UNICODE_EMOJI]
        df_emojis = pd.Series(df_emojis).value_counts()
        df_emojis = df_emojis.sort_values(ascending = False)        
        return df_emojis

    def number_of_emojies(self, text):
        """ Function that count the number of emojies in a text. """
        counter = 0
        for character in text:
            if character in UNICODE_EMOJI:
                counter += 1
        return counter

    def count_chars(self, text):
        """ Function that count the number of characters in a text excluding spaces. """
        return len(text) - text.count(" ")

    def perc_puntuation(self, text):
        """ Function that compute the percentage of puntation of a text. """
        punt_cnt = sum([1 for char in text if char in string.punctuation])
        return round(punt_cnt / (len(text) - text.count(" ")),3)*100

# ==============================================================================================================
class nlgMarkov(nlp_tools):
    """
    Natural Language Generation using Markov Chains n-gram model.
    Methods
    ---------
    learn: Learn from tokens
    generate: Generate n predicted words.

    Parameters
    ------------
    corpus: list
        Coulb be: 
        * List with all sentences as strings. Ex: ["sentence 1", "sentence 2", ...]
        * if the corpus is a long text then: ["this is the long text"]
        * List of all tokens by sentence [["hola", "soy", "juan"], ["hola", "juan"]]
    
    preprocess: Boolean
        True if each sentence in corpus needs to be preprocced first (lowercase)
        False: if the sentences in corpus are already preprocessed

    tokenize: Boolean
        True: if each sentence in corpus needs to be tokenized
        False: if the sentences in corpus are already tokenized

    tokenize_type: String
        See documentations for tokenize_text.__doc__ in class nlp_tools

    Note
    ------
    Code adapted from https://github.com/GeorgeDittmar/Mimic/blob/master/markov/MarkovChain.py
    """
    
    def __init__(self, corpus, preprocess = True, tokenize = True, tokenize_type = "word"):
        nlp_tools.__init__(self)
        self.model = None
        self.n = None
        self.corpus = corpus

        self.START_CARD = "#START#"
        self.END_CARD = "#END#"
                   
        if preprocess and tokenize:
            self.tokens = [self.tokenize_text(self.preprocess_text(sentence), tokenize_type) for sentence in tqdm(self.corpus)]
        elif preprocess and not tokenize:
            self.tokens = [self.preprocess_text(sentence) for sentence in tqdm(self.corpus)]
        elif not preprocess and tokenize:
            self.tokens = [self.tokenize_text(sentence, tokenize_type) for sentence in tqdm(self.corpus)]
        else:
            self.tokens = self.corpus

        # Add "#START#" and "#END#" cards to tokens by sentence
        self.tokens =  [[self.START_CARD] + tokens + [self.END_CARD] for tokens in self.tokens]

        
    def learn(self, n=2):
        """ Learn from n-gram models
        Parameters
        ------------
        n: integer
            number of grams to use
        """
        if n < 1:
            raise Exception("n must be greater or equal to 1")
        
        model = {}
        self.n = n

        # For all sentences incorpus (tokenized)
        for tokens in tqdm(self.tokens): 
            # For each n-gram in tokens
            for i in range(0, len(tokens) - n):
                gram = tuple(tokens[i:i + n])
                token = tokens[i + n]
                if gram in model:
                    model[gram].append(token)
                else:
                    model[gram] = [token]

        self.model = model
        return model

    def generate(self, max_tokens=100, seed=None, seed_start=True):
        """ Generate text from Markov model with size max_tokens."""

        if not self.model or not self.n:
            raise Exception("Error: There is no model. Run first learn().")

        # Select seed only from tuples that start with "#START#"
        if seed is None:
            if seed_start:
                seed = random.choice([k for k in list(self.model.keys()) if k[0]==self.START_CARD])
            else:
                seed = random.choice([k for k in list(self.model.keys()) if k[0]!=string.punctuation])

        output = list(seed)
        current = seed

        # For all tokens selected
        for i in range(self.n, max_tokens):
            # get next possible set of words from the seed word
            if current in self.model:
                choice = random.choice(self.model[current])
                output.append(choice)
                current = tuple(output[-self.n:])
                if choice is self.END_CARD: 
                    break
            else:
                if current[-1] not in string.punctuation:
                    output.append('.')
                current = random.choice(list(self.model.keys()))

        output_sentence = ' '.join([o for o in output if (o != self.START_CARD) and (o != self.END_CARD)]) #
        output_sentence = output_sentence.capitalize()
        output_sentence = re.sub(r' , ', ', ', output_sentence)
        output_sentence = re.sub(r' \. ', '. ', output_sentence)
        output_sentence = re.sub(r' \.', '.', output_sentence)
        output_sentence = re.sub(r' ; ', '; ', output_sentence)
        output_sentence = re.sub(r'\.{2,}', '.', output_sentence)
        output_sentence = re.sub("(^|[.?!])\s*([a-zA-Z])", lambda p: p.group(0).upper(), output_sentence)   
        
        return dict(tokens = output, sentence = output_sentence)

# ==============================================================================================================
class classification_battery():

    """
    This class contains a set of methods that allow to perform different models in a Text Classification problem. 
    It can be used to predict autors from text, the person that wrote a message in chats, intent classification, ...

    Parameters
    -------------
    - X_d: List
        Array with all the text sentences. Ex: ["Hola", "Cómo te va?", "Adiós"]
    - y_d: List
        Array with all the labels paired ont-to-one with X_d. Ex: ["saludo", "saludo", "despedida"]
    - config: Dictionary
        Diccionario de configuraciones
        self.config = {
            "print"          : Boolean, default: True
                True if want to verbose
            "lang"           : String, default: spanish
                Language used: One of: "spanish", "english"
            "test_size"      : Float, default: 0.3
                Size of test dataset: ex: 0.1, 0.3 ...,
            "vectorization"  : String, default: "tf-idf"
                Type of vectorization. One of: "tf-idf" "bag-of-words" "hashing".
            "n_gram"         : string, default: "word"
                Type of n_gram, one of: 'word', 'char', 'char_wb'
            "n_range"        : tuple, default: (3,5)
                Range of n_gram: Ex: (1,1), (1,2), (1,3), (1,4), (1,5), (2,3), ... ,
            "multiclass_avg" : string, default: 'auto'
                Type of target, one of [None, 'micro', 'macro', 'weighted', 'binary', 'auto'],
            "models"         : list
                List of dictionaries with keyes "name" and "model", with the models to be tested.
                default:   [
                    {"name": "KNN (baseline)", "model" : KNeighborsClassifier(n_neighbors=3)},
                    {"name": "Naive Bayes", "model" : MultinomialNB()}, 
                    {"name": "Logistic Regression", "model" : LogisticRegression()},
                    {"name": "Stochastic Gradient Descent", "model" : SGDClassifier()}
                ]
        }
    - from_pickle: string
        Use the path of the pickle file model saved using method save_models()
        example: 'my_results.pckl' or './models/my_results.pckl'
    
    Example
    ---------
    Xfeatures = ["Hola", "Cómo te va?", "Adiós", "chaito", "chaos"]
    ylabels   = ["saludo", "saludo", "despedida", "despedida", "despedida"]
    config = {
            "print"         : True,
            "lang"          : "spanish",
            "test_size"     : 0.1,
            "vectorization" : "tf-idf",
            "n_gram"        : "word",
            "n_range"       : (1,1)
        }
    cls_bat = classification_battery(Xfeatures, ylabels, config)

    """
    
    cv_list    = []
    model_list = []
    model_lbl  = []
    consensus_name = 'Consensus Model (VotingClassifier)'
    defaultModels = [
        {"name": "KNN", "model" : KNeighborsClassifier(n_neighbors=3)},
        {"name": "Naive Bayes", "model" : MultinomialNB()}, 
        {"name": "Logistic Regression", "model" : LogisticRegression()},
        {"name": "Stochastic Gradient Descent", "model" : SGDClassifier()}
    ]

    def __init__(self, X_d=[], y_d=[], config = {}, from_pickle=''):

        if from_pickle == '':        
            self.config={}
            self.config["print"] = True if "print" not in config.keys() else config["print"]
            self.config["lang"] = "spanish" if "lang" not in config.keys() else config["lang"]
            self.config["test_size"] = 0.3 if "test_size" not in config.keys() else config["test_size"]
            self.config["vectorization"] = "tf-idf" if "vectorization" not in config.keys() else config["vectorization"]
            self.config["n_gram"] = "char_wb" if "n_gram" not in config.keys() else config["n_gram"]
            self.config["n_range"] = (1,3) if "n_range" not in config.keys() else config["n_range"]
            self.config["multiclass_avg"] = 'auto' if "multiclass_avg" not in config.keys() else config["multiclass_avg"]
            self.config["models"] = self.defaultModels if "models" not in config.keys() else config["models"]
            # Grid search with cross validation
            self.config["grid_search_cv"] = True
            
            # C: List of reguralizarion values to cross-validate over for C-SVM.
            # kernel: Specifies the kernel to use with C-SVM.
            # gamma: Gamma parameter of the C-SVM.            
            # max_cross_validation_folds: Cross folds to use duringintent training, this specifies the max number of folds.
            # scoring_function: Scoring function used for evaluating the hyper parameters. Name or function
            # This values is used with the hyperparameter in GridSearchCV
            parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10], "gamma": [0.1], "max_cross_validation_folds": 5, "scoring_function": "f1_weighted"}

            self.X_data = X_d
            self.y_data = y_d

            self.models = None
            self.voting_classifier = None

            self.unique_labels = list(set(self.y_data))
            if self.config["multiclass_avg"] == 'auto':
                self.config["multiclass_avg"] = 'binary' if len(self.unique_labels) == 2 else 'macro'
        else:
            self.load_models(from_pickle)

        self.select_vectorizer()

    def select_vectorizer(self):
        """Vectorize the data""" 

        if self.config["vectorization"] == "bag-of-words":
            if self.config["n_gram"] != "":
                self.vectorizer = CountVectorizer(analyzer = self.config["n_gram"], ngram_range = self.config["n_range"])  # CountVectorizer(stop_words=the_stop_words)
            else:
                self.vectorizer = CountVectorizer()
        elif self.config["vectorization"] == "tf-idf":
            if self.config["n_gram"] != "":
                self.vectorizer = TfidfVectorizer(analyzer = self.config["n_gram"], ngram_range = self.config["n_range"]) 
            else:
                 self.vectorizer = TfidfVectorizer()
        elif self.config["vectorization"] == "hashing":
            if self.config["n_gram"] != "":
                self.vectorizer = HashingVectorizer(analyzer = self.config["n_gram"], ngram_range = self.config["n_range"])
            else:
                self.vectorizer = HashingVectorizer()
        else:
            print("Default vectorization used: Bag-of-Words")
            self.vectorizer = CountVectorizer()

    def set_vectorizer(self, vectorizer):
        """ Set custom vectorizer to the model must be from sklearn"""
        self.vectorizer = vectorizer
        
    def transform_label(self, serie_lst, label_lst = []):
        """ Function that transform the categorical values of serie_lst into numerical values. 
        Parameters
        -------------
        - serie_lst: List
            List of all labels Ex: ["red", "red", "blue", "blue"]
        - label_lst: List, optional
            List of unique lables. Ex: ["red", "blue"]

        Example
        -----------
        >>> a, b = transform_label(serie_lst=["red", "red", "blue", "blue"], ["red", "blue"])            
        >>> a, b = transform_label(serie_lst=["red", "red", "blue", "blue"])

        Return
        -------------
        indexed_labels, unique_labels_list
            Pair of values
            Example: [1, 0, 0, 0, 1, 0], ["red", "blue"]
        """

        if len(label_lst) > 0:
            return [label_lst.index(i) for i in serie_lst], label_lst
        else:
            label_lst = list(set(serie_lst)) #list(pd.Series(serie_lst).unique())
            return [label_lst.index(i) for i in serie_lst], label_lst

    def test_feature(self, df, variable, col_label):
        """ Test if the feature is good or not to predict by producing a histogram with distribution of target 
        Parameters
        -----------
        - df: Pandas DataFrame 
            Dataframe with labels and features
        - variable: String 
            Name of column name of the feature (continues variable)
        - col_label: string 
            Name of column name of the label target. (Category)

        Example
        -------- 
        plt = test_feature(df, 'my_feature', 'my_target')
        """
        for i in df[col_label].unique():
            plt.hist(df[df[col_label]==i][variable], alpha = 0.5, normed=True, label = i)
        plt.legend(loc = 'upper right')
        plt.title(f"Test of feature: {variable}")
        return plt

    def baseline(self, k_rng = 10):
        """ Function that runs all KNN models up to k_rng
        Parameters
        -----------            
        - k_rng: Number of neigbhbos. Default: 10.

        Example
        ---------
        knn_mean_error, metrics_perf =  cls_bat.baseline(k_rng=5)
        """
        Xfeatures = self.X_data
        ylabels   = self.y_data
        X  = self.vectorizer.fit_transform(Xfeatures)

        # Split the database
        x_train, x_test, y_train, y_test = train_test_split(X, ylabels, test_size = self.config["test_size"], random_state = 42)

        y_test_trans, lbls = self.transform_label(y_test)

        knn_mean_error     = []
        accuracy_lst       = []
        f1_lst             = []
        recall_lst         = []
        precision_lst      = []
        model_spec         = {}

        # Calculating error for K values between 1 and num neihbors
        for i in range(1, k_rng+1):
            knn = KNeighborsClassifier(n_neighbors=i)
            knn.fit(x_train, y_train)
            
            y_pred   = knn.predict(x_test)
            y_pred_trans, lbls = self.transform_label(list(y_pred))
            accuracy = accuracy_score(y_test_trans, y_pred_trans)
            f1       = f1_score(y_test_trans, y_pred_trans, average=self.config["multiclass_avg"])
            recall   = recall_score(y_test_trans, y_pred_trans, average=self.config["multiclass_avg"])
            pecision = precision_score(y_test_trans, y_pred_trans, average=self.config["multiclass_avg"])
            
            if self.config['print']:
                print(f"\nBaseline - KNN({i}) - Test Performance")
                print(f"Accuracy: {round(accuracy,3)} | F1: {round(f1,3)} | Recall: {round(recall,3)} | Precision: {round(pecision,3)}")

            knn_mean_error.append(np.mean(y_pred != y_test))
            accuracy_lst.append(accuracy)
            f1_lst.append(f1)
            recall_lst.append(recall)
            precision_lst.append(pecision)

        k_lst = range(1, k_rng+1)
        metrics_perf = pd.DataFrame(np.column_stack([k_lst,accuracy_lst, f1_lst, recall_lst, precision_lst]))
        metrics_perf.columns = ["K","accuracy","f1","recall","precision"]
        metrics_perf.set_index("K", inplace=True)

        plt.figure(figsize=(12, 5))
        plt.plot(k_lst, knn_mean_error, color='#333333', marker='o', markerfacecolor='#FFFFFF', markersize=7, label = "Mean Error")
        plt.title('Mean Error')
        plt.xlabel('K Value')
        plt.legend(loc = "upper left")
        plt.show()

        plt.figure(figsize=(12, 5))
        plt.plot(k_lst, accuracy_lst, color='#FFBA00', marker='o', markerfacecolor='#FFFFFF', markersize=7, label = "Accuracy")
        plt.plot(k_lst, f1_lst, color='#FF6347', marker='o', markerfacecolor='#FFFFFF', markersize=7, label = "F1")
        plt.title('Out-of-Sample Performace')
        plt.xlabel('K Value')
        plt.legend(loc = "upper left")
        plt.show()


        return knn_mean_error, metrics_perf

    def train(self):
        """ This function performs different classification models in order to check the best one."""

        Xfeatures = self.X_data
        ylabels   = self.y_data

        # Vectorize X data
        X  = self.vectorizer.fit_transform(Xfeatures)

        #the_stop_words = [t for t in stopwords.words(self.config["lang"])]        
            
        model_spec = []      

        # *** 2. Split Database
        x_train, x_test, y_train, y_test = train_test_split(X, ylabels, test_size = self.config["test_size"], shuffle=True, random_state = 42)
        
        # Save model data
        self.x_train, self.x_test, self.y_train, self.y_test = x_train, x_test, y_train, y_test

        # Transform y train/test values with indexes 
        y_train_trans, lbls = self.transform_label(y_train)
        y_test_trans, lbls = self.transform_label(y_test)

        # :::::::::::::::::::::::::::::::::
        #         MODEL FOR CONSENSUS
        # ::::::::::::::::::::::::::::::::
        # Add a Voting classifier (Majority Class Labal) to get the consensus of all models
        # The idea behind the VotingClassifier is to combine conceptually different machine learning classifiers and use a majority vote 
        # or the average predicted probabilities (soft vote) to predict the class labels. 
        # Such a classifier can be useful for a set of equally well performing model in order to balance out their individual weaknesses.
        
        # Get all model names
        model_names = [m['name'] for m in self.config["models"]]

        # Save all models into object of tuples
        models_tuples = []
        for model in self.config["models"]:
            if model["name"] != self.consensus_name:
                models_tuples.append((model["name"], model["model"]))

        # Initialize Voting Classifier
        eclf = VotingClassifier(estimators=models_tuples, voting='hard')
        self.voting_classifier = eclf

        # Update consensus model
        if self.consensus_name not in model_names:
            self.config["models"].append({'name' : self.consensus_name, 'model': eclf})
        else:
            self.config["models"][model_names.index(self.consensus_name)]['model'] = eclf
        
        # :::::::::::::::::::::::::::::::::
        #        RUN FOR EACH MODEL
        # :::::::::::::::::::::::::::::::::

        # For each model
        for model in self.config["models"]:
            # Fit model classifier
            clf = model["model"]
            clf.fit(x_train, y_train)
            # Predict Train and Test
            y_pred_train = clf.predict(x_train)
            y_pred_test = clf.predict(x_test)            
            # Trainsform labels to numeric representation
            y_pred_trans_train, lbls = self.transform_label(list(y_pred_train))
            y_pred_trans_test, lbls = self.transform_label(list(y_pred_test))
            # Get performance of Train
            train_acc_val       = accuracy_score(y_pred_trans_train, y_train_trans)
            train_f1_val        = f1_score(y_pred_trans_train, y_train_trans, average=self.config["multiclass_avg"])
            train_recall_val    = recall_score(y_pred_trans_train, y_train_trans, average=self.config["multiclass_avg"])
            train_precision_val = precision_score(y_pred_trans_train, y_train_trans, average=self.config["multiclass_avg"])
            # Get performance of Test
            test_acc_val       = accuracy_score(y_pred_trans_test, y_test_trans)
            test_f1_val        = f1_score(y_pred_trans_test, y_test_trans, average=self.config["multiclass_avg"])
            test_recall_val    = recall_score(y_pred_trans_test, y_test_trans, average=self.config["multiclass_avg"])
            test_precision_val = precision_score(y_pred_trans_test, y_test_trans, average=self.config["multiclass_avg"])

            model_spec.append({
                'model' : model, 
                'cv' : self.vectorizer, 
                'performance' : {                        
                    'train' : {'accuracy' : train_acc_val, "f1" : train_f1_val, "recall" : train_recall_val, "precision" : train_precision_val},
                    'test' :  {'accuracy' : test_acc_val, "f1" : test_f1_val, "recall" : test_recall_val, "precision" : test_precision_val}
                }
            })

            if self.config['print']:
                print(f"\n{model['name']}")            
                print(f"TRAIN: Accuracy: {round(train_acc_val,3)} | F1: {round(train_f1_val,3)} | Recall: {round(train_recall_val,3)} | Precision: {round(train_precision_val,3)}")
                print(f"TEST : Accuracy: {round(test_acc_val,3)} | F1: {round(test_f1_val,3)} | Recall: {round(test_recall_val,3)} | Precision: {round(test_precision_val,3)}")
            
        self.models = model_spec

        return model_spec

    def predict_sample(self, samples):
        """ Function that tests a sample of the text you want to classify given a Vectorizer list and a Model list. Labels are the names of the models to be printed."""

        all_predictions = []
        
        if self.models and len(self.models)>0:

            for sample in samples:              
                predictions = []
                list_pred_labels = []
                list_pred_probs = []
                consensus_prediction_label = ''

                for classifier in self.models:
                    vect = classifier['cv'].transform([sample]).toarray()
                    pred = classifier['model']['model'].predict(vect)[0]
                    try:
                        pred_proba = classifier['model']['model'].predict_proba(vect)[0]
                        max_prob = np.max(pred_proba)
                    except Exception:
                        pred_proba = []
                        max_prob = None                        
                    predictions.append({'name': classifier['model']['name'], 'probability':max_prob, 'predicted_label': pred, 'predicted_probs': pred_proba})
                    list_pred_labels.append(pred)                    
                    if max_prob != None:
                        list_pred_probs.append(max_prob)
                    if classifier['model']['name'] == self.consensus_name:
                        consensus_prediction_label = pred

                mayority = max(set(list_pred_labels), key=list_pred_labels.count)
                
                try:
                    avg_prob = np.mean(list_pred_probs)
                    max_prob = np.max(list_pred_probs)
                    min_prob = np.min(list_pred_probs)
                except Exception:
                    min_prob, max_prob, avg_prob = None, None, None

                all_predictions.append({
                    'predictions': predictions,
                    'mayority': mayority,
                    'consensus': consensus_prediction_label, 
                    'summ_probs' : {'min': min_prob, 'max': max_prob, 'avg': avg_prob}
                })
                
            return all_predictions 
        else:
            raise Exception("Run the models first. Use run() method.")


    def search_models(self, vect_list = ["bag-of-words", "tf-idf"], analizers  = ['word', 'char', 'char_wb'], n_rang_lst = [(1,1), (1,2), (1,3), (1,4), (1,5), (2,3)]):
        """ Grid search the best model iterating over vectorizers, analizers, and ranges of n-grams """

        Xfeatures = self.X_data
        ylabels   = self.y_data

        # Vectorize data
        X  = self.vectorizer.fit_transform(Xfeatures)

        # Total number of iterations
        tot = len(vect_list) * len(analizers) * len(n_rang_lst)

        output_df = []

        start = time()

        c = 1
        print(f"Grid Search Started . . .\n")
        for vectorizer_i in vect_list:
            for analizer in analizers:
                for n_rang in n_rang_lst:
                    print(f"Running model: {c} out of {tot}")
                    config = {
                        "print"         : False,
                        "lang"          : self.config['lang'],
                        "test_size"     : self.config['test_size'],
                        'multiclass_avg': self.config["multiclass_avg"],
                        "models"        : self.config["models"],
                        "vectorization" : vectorizer_i,   # "tf-idf" "bag-of-words" "hashing"
                        "n_gram"        : analizer,       # 'word', 'char', 'char_wb'
                        "n_range"       : n_rang,          # (1,1) -> Only unigram, (1,2) -> Unigram and bigram, (1,3), (1,4), (1,5), (2,3)
                    }

                    cls_bat = classification_battery(Xfeatures, ylabels, config)
                    model_spec = cls_bat.train()

                    for classifier in model_spec:
                        output_df.append([classifier['model']['name'], vectorizer_i, analizer, n_rang[0], n_rang[1], classifier['performance']['train']['accuracy'], classifier['performance']['test']['accuracy'], classifier['performance']['train']['f1'], classifier['performance']['test']['f1']])
                    c += 1

        # Report Execution Time
        end = time()
        result = end - start
        print('\n%.3f seconds' % result)

        df_performance = pd.DataFrame(output_df, columns = ["Model", "Vectorizer", "Analyzer", "n_range_I", "n_range_II", "Train-Accuracy", "Test-Accuracy", "Train-F1", "Test-F1"])
        return df_performance

    def save_models(self, file_path="models"):
        """Save all models into pickle file
        Parameters
        --------------
        - file_path: String
            File path without extension.
            Example: 'my_models' or './my_models' or './models/my_models'
        """

        if self.models and len(self.models)>0:
            data_pickle = {
                'configs' : self.config,
                'models_trained' : self.models,
                'consensus_model' : self.voting_classifier,
                'unique_labels' : self.unique_labels
            }     
            with open(f"{file_path}.pckl", "wb") as f:
                pickle.dump(data_pickle, f)
                print(f"Models saved in {file_path}.pckl")
        
            
    def load_models(self, models_file_path):
        """Load pickle file into models. 
        Parameters
        ------------
        - models_file_path: String
            Example: 'my_models.pckl' or './my_models.pckl' or './models/my_models.pckl'
        """
        data_pickle = {}
        with open(models_file_path, "rb") as f:
            while True:
                try:
                    data_pickle = pickle.load(f)
                    self.config = data_pickle['configs']
                    self.models = data_pickle['models_trained']
                    self.voting_classifier = data_pickle['consensus_model']
                    self.unique_labels = data_pickle['unique_labels']
                    print(f"Models loaded correctly!. Use predict_sample() to predict.")
                except EOFError:
                    break

        return data_pickle


# ==============================================================================================================
class SkipGramModel():
    """Skip-gram Model using torch. 
    Important Note!
    -------------
    This class is too slow to train with real data. Use wordToVec instead.

    Parameters
    -------------------
    - corpus: list
        List of sentences or documents.
        Example: ['All roses are red', 'All cats are felines', ...]
    - windows_size: integer
        The maximum distance between the current and predicted word within a sentence. 
        Example: window size of 2 means: 
               Hello        my      NAME      is        Juan
            [contex-2] [context-1] CENTER [context1] [context2]

    Example
    -------------------
    corpus = [
        'he is a king',
        'she is a queen',
        'she is in love',
        'she is mad',
        'a mountain falls',
        'paris is in france'
    ]
    SGM = SkipGramModel(corpus, windows_size = 2)
    W_embedding, W_context, W, losses = SGM.run(embedding_dim=5, epochs = 30, learning_rate = 0.001, same_weights = False)

    # he-king+she = queen
    combi = SGM.W[SGM.word2idx['he']].numpy() - SGM.W[SGM.word2idx['king']].numpy() + SGM.W[SGM.word2idx['she']].numpy()
    """
    
    def __init__(self, corpus, windows_size = 2):
        self.corpus = corpus
        self.windows_size = windows_size

        self.seed = 42

    def tokenize_corpus(self, corpus):
        return [word_tokenize(x) for x in corpus]

    def create_vocabulary(self, corpus_tokenized):
        # Vocabulary : Set of unique words in a dict form. {'a', 'falls', 'france', 'he', ... , 'she'}
        vocabulary = {word for doc in corpus_tokenized for word in doc}
        return vocabulary

    def create_index_dict(self, vocabulary):
        # word2idx   : {'is': 0, 'queen': 1, 'paris': 2, 'she': 3, 'he': 4 , ... }
        word2idx   = {w:idx for (idx, w) in enumerate(vocabulary)}
        return word2idx

    def create_index_pairs(self, word2idx, corpus_tokenized, windows_size = 2):
        """Create pairs of (center word, context word): Ex. [(the, queen), ()]"""
        idx_pairs     = []
        idx_pairs_txt = []
        for sentence in corpus_tokenized:
            indices = [word2idx[x] for x in sentence]
            for center_word_pos in range(len(indices)):
                for w in range(-windows_size, windows_size+1):
                    contex_word_pos = center_word_pos + w
                    if contex_word_pos < 0 or contex_word_pos >= len(indices) or contex_word_pos == center_word_pos:
                        continue
                    idx_pairs.append((indices[center_word_pos], indices[contex_word_pos]))
                    idx_pairs_txt.append((sentence[center_word_pos],sentence[contex_word_pos]))
        return idx_pairs

    def one_hot_enc_vect(self, word_index, vocabulary):
        """Create one-hot-encoding representation from index and vocavulary."""
        x = torch.zeros(len(vocabulary)).float()
        x[word_index] = 1.0
        return x

    # def train(self, embedding_dim = 5, epochs = 10, learning_rate = 0.001, same_weights = False):
    #     """Train Word2Vec Neural Network.
    #     Parameters
    #     ------------------
    #     - embedding_dim : Integer, optional
    #         Number of nodes in hidden layer (in real situations is around 300)
    #     - epochs : Integer, optional
    #         Number of epochs to run.
    #     - same_weights: Boolean
    #         True if same weights are used accross model.
    #     """

    #     # 1. Tokenize corpus
    #     self.tokenized_corpus = self.tokenize_corpus(self.corpus)
    #     # 2. Create Vocabulary
    #     self.vocabulary = self.create_vocabulary(self.tokenized_corpus)
    #     # 3. Create index dictionary of vovabulary
    #     self.word2idx   = self.create_index_dict(self.vocabulary)
    #     # 4. Create index pairs (CENTER WORD, CONTEXT WORD)
    #     self.idx_pairs  = self.create_index_pairs(self.word2idx, self.tokenized_corpus, self.windows_size)

    #     # embedding_dim : Number of nodes in hidden layer (in real situations is around 300)
    #     torch.manual_seed(self.seed)
    #     # Start the weights randomly
    #     W_embedding = Variable(torch.randn(embedding_dim, len(self.vocabulary)).float(), requires_grad = True)

    #     if same_weights:
    #         W_context = torch.t(W_embedding)
    #     else:
    #         W_context   = Variable(torch.randn(len(self.vocabulary), embedding_dim).float(), requires_grad = True)
        

    #     losses = []

    #     # For each epoch
    #     for ep in tqdm(range(epochs)):
    #         #print(f"\n****************************************")
    #         #print(f"---------- Epoch: {ep} of {epochs} -----------")
    #         loss_val = 0
    #         # For each pair of center_word (input), context word (target label)
    #         for input_word, target in self.idx_pairs:
    #             #print(f"Pairs: {input_word} | {target}")
    #             x_input = Variable(self.one_hot_enc_vect(input_word, self.vocabulary).float())
    #             y_true  = Variable(torch.from_numpy(np.array([target])).long())

    #             # 1. CREATION OF INPUT WORD EMBEDDING - HIDDEN LAYER
    #             # Multiplication of W_embedding [embedding_dim, len(vocabulary)] X x_input [len(vocabulary), 1] = z1 [embedding_dim, 1]
    #             z1 = torch.matmul(W_embedding, x_input)
                
    #             # 2. CREATION OF Z SCORE FOR EACH WORD IN THE VOCABULARY
    #             # Multiplication of W_context [len(vocabulary), embedding_dim] X z1 [embedding_dim, 1] = z2 [len(vocabulary), 1]
    #             z2 = torch.matmul(W_context, z1)

    #             # 3. APPLY THE SOFTMAX FUNCTION TO THE Z2 VECTOR 
    #             # Soft max is basically a normalization of a vector between 0,1 using a exponential.  {EXP()} / {SUM EXP()}
    #             log_soft_max = F.log_softmax(z2, dim = 0)

    #             # 4. COMPUTE THE NEGATIVE-LOG-LIKELIHOOD LOSS
    #             # Compute the loss comparing the log_soft_max and the y_true value of the context. (This makes the algorithm to learn)
    #             loss = F.nll_loss(log_soft_max.view(1,-1), y_true)
    #             loss_val += loss.item()

    #             # Compute Gradient
    #             loss.backward()

    #             # 5. UPDATE EMBEDDINGS (LEARN)
    #             # If in the output after the softmax we find that the entry for the context word is the biggest one then the loss is small. 
    #             # Otherwise, the loss should be bigger in order the weights to adjust and learn. 
    #             W_embedding.data = W_embedding - (learning_rate * W_embedding.grad.data)

    #             if same_weights == False:
    #                 W_context.data   = W_context - (learning_rate * W_context.grad.data)

    #             W_embedding.grad.data.zero_()

    #             if same_weights == False:
    #                 W_context.grad.data.zero_()

    #             #print(f"Loss: {round(loss_val/len(idx_pairs),4)}\n")
            
    #         losses.append(loss_val/len(self.idx_pairs))

    #     if same_weights == False:
    #         W = W_embedding + torch.t(W_context)
    #         W = (torch.t(W)/2).clone().detach()
    #     else:
    #         W = W_embedding

    #     self.W_embedding = W_embedding
    #     self.W_context   = W_context
    #     self.W           = W
    #     self.losses      = losses

    #     return W_embedding, W_context, W, losses

    # def plot_loss(self):
    #     """Function that plot the losses after training the model."""
    #     x_axis = [x+1 for x in range(len(self.losses))]
    #     plt.plot(x_axis, self.losses, '-g', linewidth = 1, label = 'Train')
    #     plt.xlabel('Epochs')
    #     plt.ylabel('Loss')
    #     plt.legend(loc = 'best')
    #     plt.show()

    # def distance_btwn_words(self, word_1, word_2):
    #     """Computes the distance (eucledian) between two word. The lower the number the more close are those words.
    #     Parameters
    #     --------------
    #     - word_1: String
    #         First Word to compare with
    #     - word_2: String
    #         Second Word to compare with
    #     """

    #     word1 = self.W[self.word2idx[word_1]].numpy()
    #     word2 = self.W[self.word2idx[word_2]].numpy()
    #     return euclidean_distances([word1], [word2])[0][0]

    # def distance_matrix(self, normalized = False):
    #     """Computes the distance matrix between all words and returns as numpy array. The lower the number the more close are those words.
    #     Parameters
    #     ---------------
    #     - normalized: Boolean
    #         True if want to normalize the matrix usin the max distance. In this case 0 means really close and 1 really far away.
    #     """

    #     df1 = np.zeros((len(self.vocabulary), len(self.vocabulary)))
    #     for idx1, v1 in enumerate(self.vocabulary):
    #         for idx2, v2 in enumerate(self.vocabulary):
    #             dist = self.distance_btwn_words(v1,v2)
    #             df1[idx1, idx2] = dist
    #     df = pd.DataFrame(data=df1, index=[v for v in self.vocabulary], columns=[v for v in self.vocabulary])
    #     self.dist_matrix = df
    #     if normalized:
    #         df_norm = df/df.max().max()
    #         return df_norm
    #     else:
    #         return df

    # def get_similarity(self, word, top=10, normalized=False):
    #     """Get words that are similar (close in distance) to the word.
    #     Parameters
    #     ---------------
    #     - word: String
    #         Word that is included in the vocabulary.
    #     """

    #     mat_dist = self.distance_matrix(normalized)
    #     matches = mat_dist[word].sort_values(ascending=True).head(top).to_dict()
    #     results=[]
    #     for x in matches:
    #         if x != word:
    #             results.append((x,matches[x]))
    #     return results

    # def get_similarity_from_embedding(self, word_embedding, top=10):
    #     """Get words that are similar (close in distance) to the word in vector representation.
    #     Parameters
    #     ---------------
    #     - word_embedding: List
    #         Vector representation of a word. Must have same dimentions as vocavulary. Ex: [0.123, 0.531, 0.123, ....].
    #     """

    #     distances = []
    #     for w_i in self.word2idx:
    #         d = euclidean_distances([word_embedding], [self.W[self.word2idx[w_i]].numpy()])
    #         distances.append((w_i, d[0][0]))

    #     df = pd.DataFrame(distances)
    #     df.columns = ['Word','Distance']
    #     df.set_index('Word', inplace=True)
    #     df.sort_values('Distance')

    #     matches = df.head(top).to_dict()
    #     matches = matches['Distance']
    #     results=[]
    #     for x in matches:
    #         results.append((x,matches[x]))

    #     return results


if __name__ == "__main__":
    pass
    # ------ Example of NLG with markov chains
    #nlgMk = nlgMarkov(["Hola!, esto es una prueba.", "Hola mi nombre es Juan"], preprocess=True, tokenize = True)
    #nlgMk = nlgMarkov(["hola!, esto es una prueba.", "hola mi nombre es juan"], preprocess=False, tokenize = True)
    #nlgMk = nlgMarkov([["hola", "!", "esto", "es", "una", "prueba"], ["hola", "mi", "nombre" ,"es", "juan"]], preprocess=False, tokenize = False)
    # nlgMk = nlgMarkov(["The dog jumped over the moon. The dog is funny."], preprocess=True, tokenize = True)
    # print(nlgMk.tokens)
    # nlgMk.learn(n=0)
    # print("\n")
    # print(nlgMk.model)

    # nlgMk = nlgMarkov([
    #         "El aprendizaje automático o aprendizaje automatizado o aprendizaje de máquinas (del inglés, machine learning) es el subcampo de las ciencias de la computación y una rama de la inteligencia artificial, cuyo objetivo es desarrollar técnicas que permitan que las computadoras aprendan. Se dice que un agente aprende cuando su desempeño mejora con la experiencia; es decir, cuando la habilidad no estaba presente en su genotipo o rasgos de nacimiento.1​ De forma más concreta, los investigadores del aprendizaje de máquinas buscan algoritmos y heurísticas para convertir muestras de datos en programas de computadora, sin tener que escribir los últimos explícitamente. Los modelos o programas resultantes deben ser capaces de generalizar comportamientos e inferencias para un conjunto más amplio (potencialmente infinito) de datos.",
    #     ], preprocess=True, tokenize = True)
    # nlgMk.learn(n=3)
    # textGenerated = nlgMk.generate(15, seed=None, seed_start=False)
    # print(textGenerated["sentence"])


    # ------ Example of NLP tools class
    # txt_tool = nlp_tools(lang = 'spanish') 
    # print(txt_tool.top_ngram(["Hi Im Juan", "Hello, Im Maria", "Nice to meet you"], 2))
    # print(f"Emojis: {txt_tool.number_of_emojies(txt_data)}")

    # txt_data = "Hola 🍕, Soy Juan Camilo esto es una prueba de lo un texto que NecEsiista ser pre-processado! 🌭 jajajajaja"
    # clean_txt = txt_tool.preprocess_text(
    #     txt_data
    #     , lowercase= True
    #     , rem_stopwords= True
    #     , lemmatize= False
    #     , remove_html = False
    #     , remove_puntuation = True
    #     , domain_sp_stopwrd=['media','omitted','missed','voice','call']
    #     , regex_sub=['ja+']
    # )
    # print(txt_data)
    # print(clean_txt)    
    