## generate supervised features via keywords.
## idea:
## group docs by classes
## for each class, find keywords,
## score w.r.t., class presence, sort, take topn
### relation extractor
## https://conceptnet.io/
## https://github.com/commonsense/conceptnet5/wiki/Downloads

import logging
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

import gzip
import pandas as pd
import networkx as nx
import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk


class ConceptFeatures:
    """
    Core class describing sentence embedding methodology employed here.
    """
    def __init__(self,
                 max_features=10000,
                 targets=None,
                 knowledge_graph="memory/conceptnet.txt.gz"):

        self.max_features = max_features
        self.targets = targets
        ## TODO -> download conceptnet if not present.

        self.knowledge_graph = knowledge_graph
        self.feature_names = None

    def concept_graph(self, document_space, graph_path):
        """
        If no prior knowledge graph is supplied, one is constructed.
        """

        present_tokens = set()
        for document in document_space:
            tokens = nltk.word_tokenize(document)
            tokens = [word.lower() for word in tokens]
            for token in tokens:
                present_tokens.add(token)

        grounded = []
        with gzip.open(graph_path, "rt", encoding="utf-8") as gp:
            for line in tqdm.tqdm(gp, total=34074917):
                parts = line.split()
                if len(parts) != 3:
                    # invalid triplet for the purpose of this work.
                    continue

                r, c1, c2 = parts
                r = r.split("/")[-1]
                c1 = c1.split("/")[3]
                c2 = c2.split("/")[3]
                if c1 in present_tokens and c2 in present_tokens:
                    if c1 != c2:
                        grounded.append((c1, r, c2))
        logging.info("The number of grounded relations is: {}".format(
            len(grounded)))
        return grounded

    def get_propositionalized_rep(self, documents):

        G = nx.DiGraph()
        for (s, p, o) in tqdm.tqdm(self.grounded_triplets):
            G.add_edge(s, o, type=p)
        numbered_links = {e: enx for enx, e in enumerate(G.edges())}
        set(G.nodes())
        if self.feature_names is None:
            self.feature_names = [
                e[2]['type'] + "(" + e[0] + "," + e[1] + ")"
                for e in G.edges(data=True)
            ]
            self.feature_types = [e[2]['type'] for e in G.edges(data=True)]
        rbags = []
        for enx2, document in tqdm.tqdm(enumerate(documents),
                                        total=len(documents)):
            tokens = nltk.word_tokenize(document)
            tokens = [word.lower() for word in tokens]
            doc_tokens = set(tokens)
            present = doc_tokens.intersection(G.nodes())
            subgraph = G.subgraph(present)
            rb = []
            for edge in subgraph.edges(data=True):
                enx1 = numbered_links[(edge[0], edge[1])]
                enx1 = self.feature_names[enx1]
                rb.append(enx1)
            rbags.append(" ".join(rb))
        return rbags

    def fit(self, text_vector, refit=False):
        """
        Fit the model to a text vector.
        """

        if self.knowledge_graph is None:
            self.knowledge_graph = knowledge_graph

        logging.info("Constructing the token graph.")
        sentences_separated = []
        for doc in text_vector:
            sentences = nltk.tokenize.sent_tokenize(doc)
            for els in sentences:
                sentences_separated.append(els)
        self.grounded_triplets = self.concept_graph(sentences_separated,
                                                    self.knowledge_graph)
        logging.info("Relation propositionalization ..")

        # this identifies relational bags that are grounded + stores the info
        conc_docs = self.get_propositionalized_rep(text_vector)
        logging.info("Concept-based features extracted.")
        self.concept_vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=self.max_features,
            token_pattern=r'\S+').fit(conc_docs)

    def transform(self, text_vector):
        """
        Transform the data into suitable form.
        """
        text_vector = self.get_propositionalized_rep(text_vector)
        return self.concept_vectorizer.transform(text_vector)

    def get_feature_names(self):

        return self.concept_vectorizer.get_feature_names()

    def fit_transform(self, text_vector, b=None):
        """
        A classifc fit-transform method.
        """

        self.fit(text_vector, self.targets)
        return self.transform(text_vector)


if __name__ == "__main__":

    example_text = pd.read_csv("../data/insults/train.tsv", sep="\t")
    text = example_text['text_a']
    labels = example_text['label']

    rex = ConceptFeatures()
    rex.fit(text)
    m = rex.transform(text)
    print(m.shape)
    fnames = rex.get_feature_names()
