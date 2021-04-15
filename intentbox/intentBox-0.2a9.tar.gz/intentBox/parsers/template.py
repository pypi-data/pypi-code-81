import abc
import re
from intentBox.utils import flatten, normalize
from intentBox.segmenter import Segmenter
from intentBox.coreference import replace_coreferences

import enum


class IntentStrategy(str, enum.Enum):
    SINGLE_INTENT = "single"
    REMAINDER = "remainder"
    SEGMENT = "segment"
    SEGMENT_REMAINDER = "segment+remainder"
    SEGMENT_MULTI = "segment+multi"


class IntentExtractor:
    def __init__(self, lang="en-us", use_markers=True, solve_corefs=True,
                 config=None, strategy=IntentStrategy.SEGMENT_REMAINDER):
        self.config = config or {}
        self.solve_corefs = solve_corefs
        self.segmenter = Segmenter(lang=lang, use_markers=use_markers,
                                   solve_corefs=solve_corefs)
        self.lang = lang
        self.strategy = strategy

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

        if confidence is below min_conf intent is None

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
        if self.solve_corefs:
            utterance = replace_coreferences(utterance)

        if self.strategy in [IntentStrategy.SEGMENT_REMAINDER,
                             IntentStrategy.SEGMENT]:
            utterances = self.segmenter.segment(utterance)
            # up to N intents
        else:
            utterances = [utterance]
        prev_ut = ""
        bucket = []
        for utterance in utterances:
            # calc intent + calc intent again in leftover text
            if self.strategy in [IntentStrategy.REMAINDER,
                                 IntentStrategy.SEGMENT_REMAINDER]:
                intents = self.intent_remainder(utterance)  # up to 2 intents

                # use a bigger chunk of the utterance
                if not intents and prev_ut:
                    # TODO ensure original utterance form
                    # TODO lang support
                    intents = self.intent_remainder(prev_ut + " " + utterance)
                    if intents:
                        # replace previous intent match with
                        # larger utterance segment match
                        bucket[-1] = intents
                        prev_ut = prev_ut + " " + utterance
                else:
                    prev_ut = utterance
                    bucket.append(intents)

            # calc single intent over full utterance
            # if this strategy is selected the segmenter step is skipped
            # and there is only 1 utterance
            elif self.strategy == IntentStrategy.SINGLE_INTENT:
                bucket.append([self.calc_intent(utterance)])

            # calc multiple intents over full utterance
            # "segment+multi" is misleading in the sense that
            # individual intent engines should do the segmentation
            # if this strategy is selected the segmenter step is skipped
            # and there is only 1 utterance
            else:
                intents = [intent for ut, intent in
                           self.calc_intents(utterance).items()]
                bucket.append(intents)

        return [i for i in flatten(bucket) if i]

    def manifest(self):
        # TODO vocab, skill ids, intent_data
        return {
            "intent_names": []
        }


