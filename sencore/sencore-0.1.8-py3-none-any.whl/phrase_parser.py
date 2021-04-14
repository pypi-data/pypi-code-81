import spacy
from sencore.parser import Parser
from spacy import Language
from phrase_detective import NounPhraseRecognizer, PrepPhraseRecognizer, VerbKnowledgeRecognizer, PKG_INDICES
from sencore.lib import extend_ranges

@Language.factory("nprecog")
def create_np_parser(nlp: Language, name: str):
  """Register ``NounPhraseRecognizer`` into pipeline with component name ``nprecog``
  """
  return NounPhraseRecognizer(nlp) 

@Language.factory("pprecog")
def create_pp_parser(nlp: Language, name: str):
  """Register ``PrepPhraseRecognizer`` into pipeline with component name ``pprecog``
  """
  return PrepPhraseRecognizer(nlp) 

@Language.factory("vkbrecog")
def create_vkb_parser(nlp: Language, name: str):
  """Register ``VerbKnowledgeRecognizer`` into pipeline with component name ``vkbrecog``
  """
  return VerbKnowledgeRecognizer(nlp) 

class PhraseParser(Parser):
  """``PhraseParser`` is to detect phrases from sentence. Inherit ``Parser``, implements ``digest``.
  """

  def __init__(self, lang):
    """Initialize nlp processor according to language

    Args:
      lang (str): language abbreviation
    """

    super().__init__(lang) 
    self._nlp = spacy.load(PKG_INDICES[lang])
    self._nlp.add_pipe("nprecog")
    self._nlp.add_pipe("pprecog")
    self._nlp.add_pipe("vkbrecog")

  def digest(self, sentence):
    """Parse sentence into phrases with linguistic meta info

    Args:
      sentence (str): sentence to be parsed

    Returns:
      dict: Keys are ``noun_phrase``, ``prep_phrases``, ``verbs``, ``passive_phrases``, ``verb_phrases``
    """


    doc = self._nlp(sentence)
    
    noun_phrases = [np.text for np in doc._.noun_phrases]
    prep_phrases = [pp.text for pp in doc._.prep_phrases]
    verbs = [{"text": v.text, "tag": v.tag_, "form": spacy.explain(v.tag_), "lemma": v.lemma_} for v in doc._.verbs]
    passive_phrases = [pp.text for pp in doc._.passive_phrases]
    verb_phrases = doc._.verb_phrases

    # In order to mark the span as noun_phrases, verb_phrases, verbs or plain for subtitle usage
    noun_phrases_ranges = [(np.start, np.end, "noun_phrases") for np in doc._.noun_phrases]
    prep_phrases_ranges = [(pp.start, pp.end, "prep_phrases") for pp in doc._.prep_phrases]
    verbs_ranges = [(v.i, v.i+1, "verbs") for v in doc._.verbs]

    doc_mark = extend_ranges(noun_phrases_ranges+prep_phrases_ranges+verbs_ranges, len(doc))
    markers = [(doc[d[0]: d[1]].text, d[2]) for d in doc_mark]

    return {
      "noun_phrases": noun_phrases,
      "prep_phrases": prep_phrases,
      "verbs": verbs,
      "passive_phrases": passive_phrases,
      "verb_phrases": verb_phrases,
      "markers": markers
    }

