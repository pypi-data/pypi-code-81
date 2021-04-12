# -*- coding:utf-8 -*-
# CREATED BY: jiangbohuai
# CREATED ON: 2021/4/8 11:04 AM
# LAST MODIFIED ON:
# AIM:
import unittest
from sentence_spliter.spliter import cut_to_sentences_en
from sentence_spliter.logic_graph_en import long_cuter_en
from sentence_spliter.automata.sequence import EnSequence
from sentence_spliter.automata.state_machine import StateMachine


class test_spliter(unittest.TestCase):
    def test_bug_2021_4_10(self):
        paragraph = "Some of the fellows pretended to think I was mad when I rushed at Chandos and hugged him, and shouted, \"It's all your doing, old fellow. I'm going to sea! I'm going to sea!\""
        __long_machine_en = StateMachine(long_cuter_en(min_len=6, max_len=10))
        m_input = EnSequence(paragraph)
        acutal = m_input.sentence_list()
        print(acutal)
        expect = ['The night was rapidly approaching; and already, at the cry of “Moccoletti!” '
                  'repeated by the shrill voices of a thousand vendors,',
                  ' two or three stars began to burn among the crowd.',
                  ' It was a signal. At the end of ten minutes fifty thousand lights glittered, '
                  'descending from the Palazzo di Venezia to the Piazza del Popolo,',
                  ' and mounting from the Piazza del Popolo to the Palazzo di Venezia.',
                  ' It seemed like the fête of Jack-o’-lanterns.']

        self.assertEqual(expect, acutal)