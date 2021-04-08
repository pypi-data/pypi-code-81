""" Pattern and template based chatbot dialog engines """
import logging

# import pandas as pd

from qary.etl import faqs
from qary.constants import FAQ_DOMAINS, FAQ_MIN_SIMILARITY, FAQ_MAX_NUM_REPLIES
from qary.skills.base import BotReply
from qary import spacy_language_model
from qary.etl import knowledge_extraction as extract  # noqa
import numpy as np

log = logging.getLogger(__name__)

nlp = spacy_language_model.nlp
if nlp._meta['vectors']['width'] < 300:  # len(nlp('word vector').vector) < 300:
    log.warning(f"SpaCy Language model ({nlp._meta['name']}) doesn't contain 300D word2vec word vectors.")
    nlp = spacy_language_model.nlp = spacy_language_model.load('en_core_web_md')


def capitalizations(s):
    return (s, s.lower(), s.upper(), s.title())


class Skill:
    r""" Skill that can reply with answers to frequently asked questions using data/faq/*.yml

    >>> bot = Skill()
    >>> bot.reply('What are the basic variable data types in python?')[0][1]
    '`float`, `int`, `str`, and `bool`'
    >>> bot.reply(None)
    [(0.1, 'I don\'t...
    """

    def __init__(self, domains=FAQ_DOMAINS):
        """ Load glossary from yaml file indicated by list of domain names """
        global nlp
        self.nlp = nlp
        self.faq = faqs.load(domains=domains)

    def reply(self, statement, context=None):
        """ Suggest responses to a user statement string with [(score, reply_string)..]"""
        statement = statement or ''
        responses = []
        question_vector = self.nlp(statement).vector
        log.debug(f"question_vector is {question_vector}")
        question_vector /= np.linalg.norm(question_vector)
        log.debug(f"faq['question_vectors'].shape is {self.faq['question_vectors'].shape}")
        question_similarities = self.faq['question_vectors'].dot(question_vector.reshape(-1, 1))
        idx = question_similarities.argmax()
        mask = np.array(question_similarities).flatten() >= FAQ_MIN_SIMILARITY
        # TODO: progressively expand threshold in case there are many more than FAQ_MAX_NUM_REPLIES similar Q's
        if sum(mask) >= 1:
            responses.extend(BotReply(confidence, text, skill=self.__module__) for confidence, text in
                             zip(question_similarities[mask],
                                 (str(a) for a in self.faq['answers'][mask])
                                 ))
            responses = sorted(responses, reverse=True)[:FAQ_MAX_NUM_REPLIES]
        else:
            responses = [(
                0.10,
                f"I don't know. Here's a FAQ similar to yours that you might try: \"{self.faq['questions'][idx]}\". ")]
        return responses
