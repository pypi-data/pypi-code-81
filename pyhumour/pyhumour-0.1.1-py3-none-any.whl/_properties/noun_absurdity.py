"""Implementation of the Noun Absurdity property."""

from collections import defaultdict
from functools import partial
import numpy as np
import os
import re
import sys
from scipy.spatial import distance

from pyhumour._utilities.pos_tag_bigram_frequency_matrix import POSTagBigramFrequencyMatrix


class NounAbsurdity:
    """Calculates the 'Noun Absurdity' value of a given text."""

    def __init__(self, frequency_matrix):
        """
        Construct a :class:`NounAbsurdity` object.

        :param POSTagBigramFrequencyMatrix frequency_matrix: The adjective-noun frequency matrix
        """
        self.adj_noun_dict = frequency_matrix
        self.embeddings_index = get_embeddings_index()

    def calculate(self, pos_tags: list) -> float:
        """Return the 'Humourous Noun Absurdity' value of a given text.

        :param list pos_tags: List of pos_tags for the given text.
        """
        acceptable_types = ('JJ', 'JJR', 'JJS')
        second_type = ('NN', 'NNS', 'NNP', 'NNPS')
        noun_absurdity_average = 0
        noun_absurdity_positive = 0
        noun_absurdity_count = 0
        number_of_pos_tags = len(pos_tags)
        for j in range(number_of_pos_tags-1):
            if pos_tags[j][1] in acceptable_types and pos_tags[j+1][1] in second_type:
                adj = re.sub('[^A-Za-z]*', '', pos_tags[j][0])
                adj = adj.lower()
                noun = re.sub('[^A-Za-z]*', '', pos_tags[j+1][0])
                noun = noun.lower()
                for k in self.adj_noun_dict.get_row(adj):  # gets list of nouns
                    noun_absurdity_positive += self.adj_noun_dict.cell_value(adj, k)*distance.cosine(
                        self.embeddings_index[noun], self.embeddings_index[k])
                    noun_absurdity_count += self.adj_noun_dict.cell_value(adj, k)
        if noun_absurdity_count > 0:
            noun_absurdity_average = noun_absurdity_positive / noun_absurdity_count

        return noun_absurdity_average


def get_embeddings_index():
    """Returns the ConceptNet Embeddings-Index matrix."""
    embeddings_index = defaultdict(partial(np.ndarray, 0))
    resources_path = os.path.join(os.path.dirname(sys.modules['pyhumour'].__file__), 'resources')
    target_path = os.path.join(resources_path, 'numberbatch-en.txt')
    try:
        f = open(target_path, encoding='utf-8')
    except FileNotFoundError:
        import requests
        import gzip
        import shutil

        url = 'https://conceptnet.s3.amazonaws.com/downloads/2019/numberbatch/numberbatch-en-19.08.txt.gz'
        download_path = os.path.join(resources_path, 'numberbatch-en-19.08.txt.gz')
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(download_path, 'wb') as f:
                f.write(response.raw.read())

        with gzip.open(download_path) as f_in:
            with open(target_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove(download_path)  # removes the gz (zip) file

        f = open(target_path, encoding='utf-8')

    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    return embeddings_index
