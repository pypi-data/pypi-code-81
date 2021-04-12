from intentBox.adapt_extract import AdaptExtractor
from intentBox.padaos_extract import PadaosExtractor
from intentBox.parsers.template import IntentExtractor
from intentBox.utils import LOG, resolve_resource_file


class IntentBox(IntentExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_engines()
        # optional entities automatically tagged
        # WARNING might artificially increase confidence of adapt intents and skew results
        self._auto = []

    def _load_engines(self):
        # TODO plugin system
        self.adapt = AdaptExtractor(config=self.config)
        self.padaos = PadaosExtractor(config=self.config)
        try:
            from intentBox.padatious_extract import PadatiousExtractor
            self.padatious = PadatiousExtractor(config=self.config)
        except ImportError:
            # padatious not installed (optional)
            # use a dummy engine
            self.padatious = IntentExtractor(config=self.config)

        self.adapt.segmenter = self.padaos.segmenter = \
            self.padatious.segmenter = self.segmenter

    @property
    def context_manager(self):
        return self.adapt.context_manager

    @property
    def context_keywords(self):
        return self.adapt.context_keywords

    @property
    def context_greedy(self):
        return self.adapt.context_greedy

    def add_auto_entity_from_file(self, entity_name, file_name):
        self.register_adapt_entity_from_file(entity_name, file_name)
        self.register_padatious_entity_from_file(entity_name, file_name)

    def register_adapt_intent(self, intent_name, samples=None, optional_samples=None):
        LOG.info("Registering adapt intent: " + intent_name)
        optional_samples = optional_samples or []
        optional_samples += self._auto
        self.adapt.register_intent(intent_name, samples, optional_samples)

    def register_adapt_entity(self, entity_name, samples=None, alias_of=None):
        LOG.info("Registering adapt entity: " + entity_name)
        self.adapt.register_entity(entity_name, samples, alias_of=alias_of)

    def register_adapt_regex_entity(self, regex_str):
        LOG.info("Registering adapt regex: " + regex_str)
        self.adapt.register_regex_entity(regex_str)

    def register_padatious_intent(self, intent_name, samples=None):
        LOG.info("Registering padatious intent: " + intent_name)
        self.padatious.register_intent(intent_name, samples)

    def register_padaos_intent(self, intent_name, samples=None):
        LOG.info("Registering padaos intent: " + intent_name)
        self.padaos.register_intent(intent_name, samples)

    def register_padatious_entity(self, entity_name, samples=None):
        LOG.info("Registering padatious entity: " + entity_name)
        self.padatious.register_entity(entity_name, samples)

    def register_padaos_entity(self, entity_name, samples=None):
        LOG.info("Registering padaos entity: " + entity_name)
        self.padaos.register_entity(entity_name, samples)

    def register_entity_from_file(self, entity_name, file_name):
        if file_name.endswith(".voc"):
            self.register_adapt_entity_from_file(entity_name, file_name)
        elif file_name.endswith(".rx"):
            self.register_adapt_regex_from_file(file_name)
        else:
            self.register_padatious_entity_from_file(entity_name, file_name)
            self.register_padaos_entity_from_file(entity_name, file_name)

    def register_adapt_regex_from_file(self, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering adapt regex file: " + file_name)
        with open(file_name) as f:
            samples = [l.strip() for l in f.readlines() if
                       l.strip() and not l.startswith("#") and not l.startswith("//")]
        for s in samples:
            self.register_adapt_regex_entity(s)

    def register_adapt_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering adapt entity file: " + file_name)
        with open(file_name) as f:
            samples = [l.strip() for l in f.readlines() if
                       l.strip() and not l.startswith("#") and not l.startswith("//")]
        self.register_adapt_entity(entity_name, samples)

    def register_padatious_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padatious entity file: " + file_name)
        try:
            self.padatious.register_entity_from_file(entity_name, file_name)
        except Exception as e:
            LOG.error("Could not register file: " + file_name)

    def register_padaos_entity_from_file(self, entity_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padaos entity file: " + file_name)
        try:
            self.padaos.register_entity_from_file(entity_name, file_name)
        except Exception as e:
            LOG.error("Could not register file: " + file_name)

    def register_intent_from_file(self, intent_name, file_name):
        if file_name.endswith(".voc"):
            self.register_adapt_intent_from_file(intent_name, file_name)
        elif file_name.endswith(".rx"):
            self.register_adapt_regex_from_file(file_name)
        else:
            self.register_padatious_intent_from_file(intent_name, file_name)
            self.register_padaos_intent_from_file(intent_name, file_name)

    def register_padatious_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padatious intent file: " + file_name)
        self.padatious.register_intent_from_file(intent_name, file_name)

    def register_padaos_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering padaos intent file: " + file_name)
        self.padaos.register_intent_from_file(intent_name, file_name)

    def register_adapt_intent_from_file(self, intent_name, file_name):
        file_name = resolve_resource_file(file_name)
        LOG.info("Registering adapt intent file: " + file_name)
        self.register_adapt_entity_from_file(intent_name, file_name)
        self.register_adapt_intent(intent_name)

    def register_intent(self, name, samples=None, optional_samples=None):
        if optional_samples:
            self.register_adapt_intent(name, samples, optional_samples)
        else:
            self.register_padatious_intent(name, samples)
            self.register_padaos_intent(name, samples)

    def detach_intent(self, intent_name):
        self.adapt.detach_intent(intent_name)
        self.padatious.detach_intent(intent_name)

    def detach_skill(self, skill_id):
        self.adapt.detach_skill(skill_id)
        self.padatious.detach_skill(skill_id)
        self.padaos.detach_skill(skill_id)

    def register_entity(self, name, samples=None):
        self.register_adapt_entity(name, samples)
        self.register_padatious_entity(name, samples)
        self.register_padaos_entity(name, samples)

    def calc_intent(self, utterance):
        # TODO plugin system
        utterance = utterance.strip() # spaces should not mess with exact matches

        # best intent
        a = self.adapt.calc_intent(utterance)

        _a = a.copy()
        if "__tags__" in _a:
            _a.pop("__tags__")
        LOG.debug("Adapt match: {intent}".format(intent=_a))

        p = self.padatious.calc_intent(utterance)

        LOG.debug("Padatious match: {intent}".format(intent=p))

        p2 = self.padaos.calc_intent(utterance)

        LOG.debug("Padaos match: {intent}".format(intent=p2))

        if p2 and p2["conf"] >= 0.8:
            return p2
        if a and a["conf"] >= 0.7:
            return a
        if p and p["conf"] >= 0.8:
            return p
        if a and a["conf"] > 0.4 or (a and p and 0 < p["conf"] < a["conf"]):
            return a
        if p and p["conf"] > 0.6:  # lots of false positives on 0.5 range
            return p
        if a and a["conf"]:  # adapt regex/context is often low confidence
            return a
        if p2 and p2["conf"] > 0.3:
            return p2
        if p and p["conf"] > 0.3:
            return p
        return None

    def manifest(self):
        return {
            "intent_names": self.adapt.manifest()["intent_names"] + self.padatious.manifest()["intent_names"],
            "adapt_intent_names": self.adapt.manifest()["intent_names"],
            "padaos_intent_names": self.padaos.manifest()["intent_names"],
            "padatious_intent_names": self.padatious.manifest()["intent_names"],
        }

    def calc_intents(self, utterance, min_conf=0.5):
        utterance = utterance.strip() # spaces should not mess with exact matches
        # segment + best intent per chunk
        bucket = {}
        for ut in self.segmenter.segment(utterance):
            bucket[ut] = self.calc_intent(ut)
        return bucket

    def calc_intents_list(self, utterance):
        utterance = utterance.strip() # spaces should not mess with exact matches
        # segment + all intents per chunk
        intents = self.adapt.calc_intents_list(utterance)
        p = self.padatious.calc_intents_list(utterance)
        p2 = self.padaos.calc_intents_list(utterance)
        for ut in p:
            intents[ut] += p[ut]
        for ut in p2:
            intents[ut] += p2[ut]
        return intents

    def intent_scores(self, utterance):
        utterance = utterance.strip() # spaces should not mess with exact matches
        return self.padatious.intent_scores(utterance) + \
               self.adapt.intent_scores(utterance) + \
               self.padaos.intent_scores(utterance)
