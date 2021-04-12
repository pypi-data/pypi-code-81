from intentBox.parsers.template import IntentExtractor
from intentBox.utils import LOG, normalize
import time
from adapt.intent import IntentBuilder
from adapt.context import ContextManagerFrame
from adapt.engine import IntentDeterminationEngine


class ContextManager:
    """
    ContextManager
    Use to track context throughout the course of a conversational session.
    How to manage a session's lifecycle is not captured here.

    # TODO this should be generalized and not used by adapt only
    """

    def __init__(self, timeout):
        self.frame_stack = []
        self.timeout = timeout * 60  # minutes to seconds

    def clear_context(self):
        self.frame_stack = []

    def remove_context(self, context_id):
        for context, ts in list(self.frame_stack):
            ents = context.entities[0].get('data', [])
            for e in ents:
                if context_id == e:
                    self.frame_stack.remove((context, ts))

    def inject_context(self, entity, metadata=None):
        """
        Args:
            entity(object): Format example...
                               {'data': 'Entity tag as <str>',
                                'key': 'entity proper name as <str>',
                                'confidence': <float>'
                               }
            metadata(object): dict, arbitrary metadata about entity injected
        """
        metadata = metadata or {}
        try:
            if len(self.frame_stack) > 0:
                top_frame = self.frame_stack[0]
            else:
                top_frame = None
            if top_frame and top_frame[0].metadata_matches(metadata):
                top_frame[0].merge_context(entity, metadata)
            else:
                frame = ContextManagerFrame(entities=[entity],
                                            metadata=metadata.copy())
                self.frame_stack.insert(0, (frame, time.time()))
        except (IndexError, KeyError):
            pass
        except Exception as e:
            LOG.exception(e)

    def get_context(self, max_frames=5, missing_entities=None):
        """ Constructs a list of entities from the context.

        Args:
            max_frames(int): maximum number of frames to look back
            missing_entities(list of str): a list or set of tag names,
            as strings

        Returns:
            list: a list of entities

        """
        try:
            missing_entities = missing_entities or []

            relevant_frames = [frame[0] for frame in self.frame_stack if
                               time.time() - frame[1] < self.timeout]

            if not max_frames or max_frames > len(relevant_frames):
                max_frames = len(relevant_frames)

            missing_entities = list(missing_entities)

            context = []
            last = ''
            depth = 0
            for i in range(max_frames):
                frame_entities = [entity.copy() for entity in
                                  relevant_frames[i].entities]
                for entity in frame_entities:
                    entity['confidence'] = entity.get('confidence', 1.0) \
                                           / (2.0 + depth)
                context += frame_entities

                # Update depth
                if entity['origin'] != last or entity['origin'] == '':
                    depth += 1
                last = entity['origin']
            result = []
            if len(missing_entities) > 0:

                for entity in context:
                    if entity.get('data') in missing_entities:
                        result.append(entity)
                        # NOTE: this implies that we will only ever get one
                        # of an entity kind from context, unless specified
                        # multiple times in missing_entities. Cannot get
                        # an arbitrary number of an entity kind.
                        missing_entities.remove(entity.get('data'))
            else:
                result = context

            # Only use the latest instance of each keyword
            stripped = []
            processed = []
            for f in result:
                keyword = f['data'][0][1]
                if keyword not in processed:
                    stripped.append(f)
                    processed.append(keyword)
            result = stripped
        except Exception as e:
            LOG.exception(e)
            return []
        #LOG.debug("Adapt Context: {}".format(result))
        return result


class AdaptExtractor(IntentExtractor):
    def __init__(self, normalize=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.normalize = normalize
        self.engine = IntentDeterminationEngine()
        self.context_config = self.config.get('context', {})
        # Context related initializations
        self.context_keywords = self.context_config.get('keywords', [])
        self.context_max_frames = self.context_config.get('max_frames', 3)
        self.context_timeout = self.context_config.get('timeout', 2)
        self.context_greedy = self.context_config.get('greedy', False)
        self.context_manager = ContextManager(self.context_timeout)

    def register_entity(self, name, samples=None, alias_of=None):
        samples = samples or [name]
        for kw in samples:
            self.engine.register_entity(kw, name, alias_of=alias_of)

    def register_regex_entity(self, regex_str):
        self.engine.register_regex_entity(regex_str)

    def register_intent(self, name, samples=None, optional_samples=None):
        """

        :param name: intent_name
        :param samples: list of required registered entities (names)
        :param optional_samples: list of optional registered samples (names)
        :return:
        """
        if not samples:
            samples = [name]
            self.register_entity(name, samples)
        optional_samples = optional_samples or []
        # structure intent
        intent = IntentBuilder(name)
        for kw in samples:
            intent.require(kw)
        for kw in optional_samples:
            intent.optionally(kw)
        self.engine.register_intent_parser(intent.build())
        return intent

    def calc_intent(self, utterance):
        utterance = utterance.strip() # spaces should not mess with exact matches
        if self.normalize:
            utterance = normalize(utterance, self.lang, True)
        for intent in self.engine.determine_intent(utterance, 100,
                                                   include_tags=True,
                                                   context_manager=self.context_manager):
            if intent and intent.get('confidence') > 0:
                intent.pop("target")
                matches = [k for k in intent.keys() if k not in ["intent_type", "confidence", "__tags__"]]
                intent["entities"] = {}
                for k in matches:
                    intent["entities"][k] = intent.pop(k)
                intent["conf"] = intent.pop("confidence")
                intent["utterance"] = utterance
                intent["intent_engine"] = "adapt"
                return intent
        return {"conf": 0, "intent_type": "unknown", "entities": {}, "utterance": utterance, "intent_engine": "adapt"}

    def calc_intents(self, utterance, min_conf=0.5):
        bucket = {}
        for ut in self.segmenter.segment(utterance):
            intent = self.calc_intent(ut)
            if intent["conf"] < min_conf:
                bucket[ut] = None
            else:
                bucket[ut] = intent
        return bucket

    def calc_intents_list(self, utterance, min_conf=0.5):
        utterance = utterance.strip() # spaces should not mess with exact matches
        bucket = {}
        for ut in self.segmenter.segment(utterance):

            if self.normalize:
                ut = normalize(ut, self.lang, True)
            bucket[ut] = []
            for intent in self.engine.determine_intent(ut, 100,
                                                       include_tags=True,
                                                       context_manager=self.context_manager):
                if intent:
                    intent.pop("target")
                    matches = [k for k in intent.keys() if k not in ["intent_type", "confidence"]]
                    intent["entities"] = {}
                    for k in matches:
                        intent["entities"][k] = intent.pop(k)
                    intent["conf"] = intent.pop("confidence")
                    intent["utterance"] = ut
                    intent["intent_engine"] = "adapt"
                    if intent["conf"] >= min_conf:
                        bucket[ut] += [intent]

        return bucket

    def intent_scores(self, utterance):
        utterance = utterance.strip() # spaces should not mess with exact matches
        bucket = []
        for intent in self.engine.determine_intent(utterance, 100,
                                                   include_tags=True,
                                                   context_manager=self.context_manager):
            if intent:
                intent.pop("target")
                matches = [k for k in intent.keys() if k not in ["intent_type", "confidence"]]
                intent["entities"] = {}
                for k in matches:
                    intent["entities"][k] = intent.pop(k)
                intent["conf"] = intent.pop("confidence")
                intent["intent_engine"] = "adapt"
                intent["utterance"] = utterance
                bucket += [intent]
        return bucket

    def intent_remainder(self, utterance, _prev=""):
        utterance = utterance.strip() # spaces should not mess with exact matches
        if self.normalize:
            utterance = normalize(utterance, self.lang, True)
        return IntentExtractor.intent_remainder(self, utterance)

    def intents_remainder(self, utterance, min_conf=0.5):
        """
        segment utterance and for each chunk recursively check for intents in utterance remainer

        :param utterance:
        :param min_conf:
        :return:
        """
        utterance = utterance.strip() # spaces should not mess with exact matches
        bucket = {}
        for utterance in self.segmenter.segment(utterance):
            if self.normalize:
                utterance = normalize(utterance, self.lang, True)
            bucket[utterance] = self.intent_remainder(utterance)
        return bucket

    def segment(self, text):
        if self.normalize:
            text = normalize(text, self.lang, True)
        return self.segment(text)

    def detach_intent(self, intent_name):
        LOG.debug("detaching adapt intent: " + intent_name)
        new_parsers = [
            p for p in self.engine.intent_parsers if p.name != intent_name]
        self.engine.intent_parsers = new_parsers

    def detach_skill(self, skill_id):
        LOG.debug("detaching adapt skill: " + skill_id)
        new_parsers = [
            p.name for p in self.engine.intent_parsers if p.name.startswith(skill_id)]
        for intent_name in new_parsers:
            self.detach_intent(intent_name)

    def manifest(self):
        # TODO vocab, skill ids, intent_data
        return {
            "intent_names": [p.name for p in self.engine.intent_parsers]
        }


if __name__ == "__main__":
    from pprint import pprint

    intents = AdaptExtractor()

    weather = ["weather"]
    hello = ["hey", "hello", "hi", "greetings"]
    name = ["name is"]
    joke = ["joke"]
    play = ["play"]
    say = ["say", "tell"]
    music = ["music", "jazz", "metal", "rock"]
    door = ["door", "doors"]
    light = ["light", "lights"]
    on = ["activate", "on", "engage", "open"]
    off = ["deactivate", "off", "disengage", "close"]

    intents.register_entity("weather", weather)
    intents.register_entity("hello", hello)
    intents.register_entity("name", name)
    intents.register_entity("joke", joke)
    intents.register_entity("door", door)
    intents.register_entity("lights", light)
    intents.register_entity("on", on)
    intents.register_entity("off", off)
    intents.register_entity("play", play)
    intents.register_entity("music", music)
    intents.register_entity("say", say)

    intents.register_intent("weather", ["weather"], ["say"])
    intents.register_intent("hello", ["hello"])
    intents.register_intent("name", ["name"])
    intents.register_intent("joke", ["joke"], ["say"])
    intents.register_intent("lights_on", ["lights", "on"])
    intents.register_intent("lights_off", ["lights", "off"])
    intents.register_intent("door_open", ["door", "on"])
    intents.register_intent("door_close", ["door", "off"])
    intents.register_intent("play_music", ["play", "music"])

    sentences = [
        "tell me a joke and say hello",
        "turn off the lights, open the door",
        "nice work! get me a beer",
        "Call mom tell her hello",
        "tell me a joke and the weather",
        "turn on the lights close the door",
        "close the door turn off the lights",
        "tell me a joke order some pizza",  # fail
        "close the pod bay doors play some music"  # fail
    ]

    print("CALCULATE SINGLE INTENT")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.calc_intent(sent))
        print("_______________________________")

    print("CALCULATE MAIN AND SECONDARY INTENTS")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.intent_remainder(sent))
        print("_______________________________")

    print("SEGMENT AND CALCULATE MAIN AND SECONDARY INTENTS")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.intents_remainder(sent))
        print("_______________________________")

    print("SEGMENT AND CALCULATE ALL INTENTS")
    for sent in sentences:
        print("UTTERANCE:", sent)
        pprint(intents.calc_intents_list(sent))
        print("_______________________________")
