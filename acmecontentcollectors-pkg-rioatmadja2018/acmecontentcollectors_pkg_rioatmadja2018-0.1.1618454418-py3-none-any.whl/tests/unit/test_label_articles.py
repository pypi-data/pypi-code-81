#!/usr/bin/env python
from acme_collectors.utils.helpers import label_article_pov, correct_spelling, get_organization_entities
import pytest 
from unittest import TestCase
from nltk.tree import Tree 
from typing import List 

class TestArticlePOV(TestCase):

    def test_pov(self): 
        current_article: str = """ 
        This man if the caliphate believes in him: Every Muslim dies a jaahilite death if he does not pledge allegiance to him !! On the other hand, 
        if this man was lost, corrupted, or infiltrated: he would be one of the most dangerous adversaries against the ummah in its history.
        """
        return self.assertEqual(label_article_pov(article=current_article), 'third_person')

    def test_correct_spelling(self): 
        return self.assertEqual(correct_spelling(article='dangerous zone'), 'dangerous zone' )  

    def test_get_organization_entities(self): 
        current_article: str = """
        This man if the caliphate believes in him: Every Muslim dies a jaahilite death if he does not pledge allegiance to him !! On the other hand, 
        if this man was lost, corrupted, or infiltrated: he would be one of the most dangerous adversaries against the ummah in its history.
        """ 
        organization_entity_tags: List[Tree] = [Tree('ORGANIZATION', [('Muslim', 'NNP')])]
        return self.assertEqual(get_organization_entities(article=current_article), organization_entity_tags)