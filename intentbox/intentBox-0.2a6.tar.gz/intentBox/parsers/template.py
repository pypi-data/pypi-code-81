import abc
import re
from intentBox.utils import flatten, normalize
from intentBox.segmenter import Segmenter


class IntentExtractor:
    def __init__(self, lang="en-us", use_markers=True, use_coref=False,
                 config=None):
        self.config = config or {}
        self.segmenter = Segmenter(lang, use_markers, use_coref)
        self.lang = lang

    def get_normalizations(self, utterance, lang=None):
        lang = lang or self.lang
        norm = normalize(utterance,
                         remove_articles=True,
                         lang=lang)
        norm2 = normalize(utterance,
                          remove_articles=False,
                          lang=lang)
        norm3 = re.sub(r'[^\w]', ' ', utterance)
        norm4 = ''.join([i if 64 < ord(i) < 128 or ord(i) == 32
                         else ''
                         for i in utterance])
        return [u for u in [norm, norm2, norm3, norm4] if u != utterance]

    @abc.abstractmethod
    def detach_skill(self, skill_id):
        pass

    @abc.abstractmethod
    def detach_intent(self, intent_name):
        pass

    @abc.abstractmethod
    def register_entity(self, name, samples):
        pass

    @abc.abstractmethod
    def register_intent(self, name, samples):
        pass

    def register_entity_from_file(self, entity_name, file_name):
        with open(file_name) as f:
            entities = f.read().split("\n")
            self.register_entity(entity_name, entities)

    def register_intent_from_file(self, intent_name, file_name):
        with open(file_name) as f:
            intents = f.read().split("\n")
            self.register_entity(intent_name, intents)

    @abc.abstractmethod
    def calc_intent(self, utterance):
        """ return intent result for utterance

       UTTERANCE: tell me a joke and say hello

        {'name': 'joke', 'sent': 'tell me a joke and say hello', 'matches': {}, 'conf': 0.5634853146417653}

        """
        pass

    @abc.abstractmethod
    def calc_intents(self, utterance, min_conf=0.5):
        """ segment utterance and return best intent for individual segments

        if confidence is bellow min_conf intent is None

       UTTERANCE: tell me a joke and say hello

        {'say hello': {'conf': 0.5750943775957492, 'matches': {}, 'name': 'hello'},
         'tell me a joke': {'conf': 1.0, 'matches': {}, 'name': 'joke'}}

        """
        pass

    @abc.abstractmethod
    def calc_intents_list(self, utterance):
        """ segment utterance and return all intents for individual segments

       UTTERANCE: tell me a joke and say hello

        {'say hello': [{'conf': 0.1405158302488502, 'matches': {}, 'name': 'weather'},
                       {'conf': 0.5750943775957492, 'matches': {}, 'name': 'hello'},
                       {'conf': 0.0, 'matches': {}, 'name': 'name'},
                       {'conf': 0.36216947883621736, 'matches': {}, 'name': 'joke'}],
         'tell me a joke': [{'conf': 0.0, 'matches': {}, 'name': 'weather'},
                            {'conf': 0.0, 'matches': {}, 'name': 'hello'},
                            {'conf': 0.0, 'matches': {}, 'name': 'name'},
                            {'conf': 1.0, 'matches': {}, 'name': 'joke'}]}

        """
        pass

    def intent_remainder(self, utterance, _prev=""):
        """
        calc intent, remove matches from utterance, check for intent in leftover, repeat

        :param utterance:
        :param _prev:
        :return:
        """
        intent_bucket = []
        original_utt = utterance
        while _prev != utterance:
            _prev = utterance

            intent = self.calc_intent(utterance)
            if intent:
                intent["utterance"] = original_utt
                intent["consumed_utterance"] = utterance
                intent_bucket += [intent]
                if intent.get("__tags__"):
                    # adapt
                    tags = []
                    for token in intent["__tags__"]:
                        # Substitute only whole words matching the token
                        tags.append(token.get("key", ""))
                        utterance = re.sub(
                            r'\b' + token.get("key", "") + r"\b", "",
                            utterance)
                    intent["consumed_utterance"] = " ".join(tags)
                elif len(intent.get("entities", {})):
                    # padatious
                    for token in intent["entities"]:
                        # TODO figure out a decent remainder logic for padatious
                        pass

        return intent_bucket

    def intents_remainder(self, utterance, min_conf=0.5):
        """
        segment utterance and for each chunk recursively check for intents in utterance remainer

        :param utterance:
        :param min_conf:
        :return:
        """
        utterances = self.segmenter.segment(utterance)
        bucket = []
        for utterance in utterances:
            bucket += self.intent_remainder(utterance)
        return [b for b in bucket if b]

    @abc.abstractmethod
    def intent_scores(self, utterance):
        pass

    def filter_intents(self, utterance, min_conf=0.5):
        """

        returns all intents above a minimum confidence, meant for disambiguation

        can somewhat be used for multi intent parsing

        UTTERANCE: close the door turn off the lights
        [{'conf': 0.5311372507542608, 'entities': {}, 'name': 'lights_off'},
         {'conf': 0.505765852348431, 'entities': {}, 'name': 'door_close'}]

        :param utterance:
        :param min_conf:
        :return:
        """
        return [i for i in self.intent_scores(utterance) if
                i["conf"] >= min_conf]

    def calc(self, utterance):
        """
        segment utterance and for each chunk recursively check for intents in utterance remainer

        :param utterance:
        :return:
        """
        utterances = self.segmenter.segment(utterance)
        prev_ut = ""
        bucket = []
        for utterance in utterances:
            intents = self.intent_remainder(utterance)
            if not intents and prev_ut:
                # TODO ensure original utterance form
                # TODO 2 - lang support
                intents = self.intent_remainder(prev_ut + " " + utterance)
                if intents:
                    bucket[-1] = intents
                    prev_ut = prev_ut + " " + utterance
            else:
                prev_ut = utterance
                bucket.append(intents)

        return flatten(bucket)

    def manifest(self):
        # TODO vocab, skill ids, intent_data
        return {
            "intent_names": []
        }


