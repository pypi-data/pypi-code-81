from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg
import re


class FrenchApostrophationPosprocess(NormalizerBase):
    NAME = "french_apostrophation_posprocess"

    DESCRIPTION_TRAINING = """"""

    DESCRIPTION_DECODING = """
        Remove spaces around french apostrophe
    """

    def __init__(self, src_lang: str, tgt_lang: str) -> None:
        super().__init__(src_lang, tgt_lang)

    def process_train(self, seg: Seg) -> None:
        pass

    def process_src_decoding(self, seg: Seg) -> None:
        pass

    def process_tgt_decoding(self, seg: Seg) -> None:
        if self.tgt_lang == 'fr':
            seg.tgt = seg.tgt.replace(" jusqu ’ ", " jusqu’").replace(" qu ’ ", " qu’").replace(" l ’ ", " l’").replace(" t ’ ", " t’").replace(" m ’ ", " m’").replace(" c ’ ", " c’").replace(" d ’ ", " d’").replace(" n ’ ", " n’").replace(" s ’ ", " s’").replace("L ’ ", "L’").replace("C ’ ", "C’").replace("D ’ ", "D’").replace("N ’ ", "N’").replace("S ’ ", "S’")
            #inches
            clean_matches = []
            matches = re.finditer(r"\d{1,2}\s?['’]\s?x\s?\d{1,2}\s?['’]", seg.tgt)
            for match in matches:
                clean_match = match.group().replace("’", '"').replace("'", '"').replace(" ", "").replace("x", " x ")
                seg.tgt = seg.tgt.replace(match.group(), clean_match)
            #time
            o_clock = "00"
            clean_match = ""
            matches = re.finditer(r"[0-2][0-9]\s?:\s?[0-5][0-9]", seg.tgt)
            for match in matches:
                exact_minutes = re.findall(r"\d{1,2}", match.group().split(":")[1])[0]
                clean_match = match.group().replace(":", 'h')
                if exact_minutes == o_clock:
                    clean_match = clean_match.replace(o_clock, " ")
                seg.tgt = seg.tgt.replace(match.group(), clean_match).replace("  ", "")

