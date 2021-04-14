from intentBox.coreference import CoreferenceSolver
from intentBox.utils import LOG, flatten
from intentBox.lang.en import SEGMENTATION_MARKERS_EN
from intentBox.lang.pt import SEGMENTATION_MARKERS_PT
from intentBox.lang import SEGMENTATION_MARKERS_PUNC


class Segmenter:
    # NOTE str.split operation, not token by token comparison
    # this means you need spaces on both sides of the marker

    # Add lang markers here for naive segmentation
    def __init__(self, lang="en-us", use_markers=True, use_coref=False):
        self.lang = lang
        self.use_markers = use_markers
        self.use_coref = use_coref
        self.segmenter = None
        self.solver = None
        if self.use_coref:
            if not lang.startswith("en"):
                LOG.error("unsupported coreference resolution language")
            else:
                self.solver = CoreferenceSolver()

    @staticmethod
    def _extract(text, markers, no_replaces=None):
        no_replaces = no_replaces or ["p.m", "p.m.", "a.m", "a.m."]
        if isinstance(text, str):
            sents = [text]
        else:
            sents = text
        for m in markers:
            for idx, sent in enumerate(sents):
                subs = {}
                if isinstance(sent, str):
                    for no in no_replaces:
                        if m in no:
                            _ = str(idx) + no.replace(m, "")
                            subs[_] = no
                            sents[idx] = sents[idx].replace(no, _)
                    splits = sents[idx].split(m)
                    for k in subs:
                        splits = [_.replace(k, subs[k]) for _ in splits]
                    sents[idx] = splits

            # flatten list
            sents = flatten(sents)
        return sents

    @staticmethod
    def extract_candidates_en(text, no_replaces=None):
        no_replaces = no_replaces or ["p.m", "p.m.", "a.m", "a.m."]
        sents = Segmenter.extract_candidates_generic(text, no_replaces)
        return Segmenter._extract(sents, SEGMENTATION_MARKERS_EN, no_replaces)

    @staticmethod
    def extract_candidates_pt(text, no_replaces=None):
        no_replaces = no_replaces or []
        sents = Segmenter.extract_candidates_generic(text)
        return Segmenter._extract(sents, SEGMENTATION_MARKERS_PT, no_replaces)

    @staticmethod
    def extract_candidates_generic(text, no_replaces=None):
        no_replaces = no_replaces or ["p.m", "p.m.", "a.m", "a.m."]
        return Segmenter._extract(text, SEGMENTATION_MARKERS_PUNC, no_replaces)

    @staticmethod
    def extract_candidates(text, lang="en"):
        if lang.startswith("en"):
            return Segmenter.extract_candidates_en(text)
        elif lang.startswith("pt"):
            return Segmenter.extract_candidates_pt(text)
        return Segmenter.extract_candidates_generic(text)

    def segment(self, text):
        if self.use_coref and self.solver:
            text = self.solver.replace_coreferences(text)
        if self.use_markers:
            text = self.extract_candidates(text, self.lang)
        return [s for s in text if s]
