""" Pattern and template based chatbot dialog engines """
import logging
import os

import pronouncing
import random
import re 

class Skill:
    r"""Returning a rhyming sentence"""

    def reply(self, statement, context=None):
        r"""Returns a sentence in which the final word rymes with the final word of the input string

        Examples:
            #TODO
        """
     
        # Removing any punctuation from the string using regex, except apostrophes
        statement = re.sub(r"[^\w\d'\s]+", '', statement) 
        word_list = statement.split() #list of words
        rhyming_words = pronouncing.rhymes(word_list[-1]) #list of words that rhyme with the last word in sentence
        if len(rhyming_words) == 0:
            return "Nothing rhymes with " + word_list[-1]
        response = ' '.join(word_list[:-1]) + ' ' + random.choice(rhyming_words)
        return [(1.0, response)]
