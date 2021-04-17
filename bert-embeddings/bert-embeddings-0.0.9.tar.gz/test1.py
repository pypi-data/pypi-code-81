import unittest
import BertEmbeddings as main

import torch

from time import time

class EmbeddingsTests(unittest.TestCase):

    def test_bert_embeddings(self):
        context = 'Denmark is a Nordic country in Northern Europe. Denmark proper, which is the southernmost of the Scandinavian countries, consists of a peninsula, Jutland, and an archipelago of 443 named islands, with the largest being Zealand, Funen and the North Jutlandic Island.'
        question = 'what is denmark'

        bert_embeddings = main.BertEmbeddings()

        t0 = time()
        bert_embeddings_output = bert_embeddings([context]*2)
        t1 = time()

        self.assertTrue(expr = t1-t0 < 0.1, msg = f'The bert_embeddings output wasn\'t fast enough. It took {t1-t0}sec when supposed to take 0.1sec. Maybe try again')

        contexts = bert_embeddings_output
        c_tokens0 = contexts[0]['tokens']
        c_sentence_tokens0 = contexts[0]['sentence_tokens']
        c_embeddings_map0 = contexts[0]['embeddings_map']

        self.assertTrue(expr = len(contexts) == 2, msg = f'Length og contexts wasn\' long enough. Output: {len(context)} \nexpected output: 2')
        self.assertTrue(expr = type(c_tokens0[0]) == str, msg = f'context Tokens didn\'t contain any strings. output dtype {type(c_tokens0[0])}')
        self.assertTrue(expr = type(c_sentence_tokens0[0]) == list, msg = f'context Sentence Tokens didn\'t contain any lists. output dtype {type(c_sentence_tokens0[0])}')
        self.assertTrue(expr = type(c_embeddings_map0) == dict, msg = f'c_embeddings_map0 wasn\'t a dictionary.\noutput: {type(c_embeddings_map0)}')
        expr = type(c_embeddings_map0[list(c_embeddings_map0)[0]]) == torch.Tensor
        self.assertTrue(expr = expr, msg = f'c_embeddings_map didn\'t contain any torch tensor. Output {type(c_embeddings_map0[list(c_embeddings_map0)[0]])}')

        try:
            for idx,token in enumerate(c_tokens0):
                _ = c_embeddings_map0[f'{token}_{idx}']
        except Exception as e:
            self.assertTrue(expr = False, msg = f'{e}\nFailing to properly create dictionary of tokens and index to access embeddings')

if __name__ == '__main__':
    unittest.main()