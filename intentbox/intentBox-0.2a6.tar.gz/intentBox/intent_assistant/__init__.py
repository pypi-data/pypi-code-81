from os.path import expanduser, isdir, isfile, join, basename
import os

from adapt.intent import IntentBuilder as AdaptBuilder
from auto_regex import AutoRegex

from intentBox.lang.en import ENGLISH_STOP_WORDS
from intentBox.lang.pt import PORTUGUESE_STOP_WORDS
from intentBox.lang import GENERIC_STOP_WORDS
from intentBox.segmentation import segment_keywords
from intentBox.utils import tokenize, normalize, expand_options, \
    expand_keywords, merge_dict, match_one


class IntentAssistant:
    def __init__(self, ignore_errors=False, stop_words=None,
                 normalize=True, lang="en"):
        self._entities = {}
        self._intents = {}
        self._regex = {}
        self.ignore_errors = ignore_errors
        self._stop_words = stop_words
        self._normalize = normalize
        self.lang = lang.lower()

    @property
    def stop_words(self):
        if self._stop_words is None:
            if self.lang.startswith("en"):
                return ENGLISH_STOP_WORDS + GENERIC_STOP_WORDS
            elif self.lang.startswith("pt"):
                return PORTUGUESE_STOP_WORDS + GENERIC_STOP_WORDS
            else:
                return GENERIC_STOP_WORDS
        return self._stop_words + GENERIC_STOP_WORDS

    @property
    def intents(self):
        return self._intents

    @property
    def entities(self):
        return self._entities

    # file handling
    def load_folder(self, path, lang=None):
        path = expanduser(path)
        if not isinstance(path, str):
            raise ValueError
        if not isdir(path):
            raise NotADirectoryError
        for root, folders, files in os.walk(path):
            if lang and not root.endswith(lang):
                continue
            for f in files:
                if self.ignore_errors:
                    self.load_file(join(root, f))
                elif f.endswith(".intent"):
                    print(f"Loading intent file: {f}")
                    self.load_file(join(root, f))
                elif f.endswith(".entity") or f.endswith(".voc") or \
                        f.endswith(".rx"):
                    print(f"Loading entity file: {f}")
                    self.load_file(join(root, f))

    def load_file(self, path):
        path = expanduser(path)
        if not isinstance(path, str):
            raise ValueError
        if isdir(path):
            raise IsADirectoryError
        if not isfile(path):
            raise FileNotFoundError
        if path.endswith(".intent"):
            self.load_intent_file(path)
        elif path.endswith(".entity") or path.endswith(".voc"):
            self.load_entity_file(path)
        elif path.endswith(".rx"):
            self.load_regex_file(path)
        else:
            print("ERROR: unknown file format {}".format(path))
            raise ValueError

    # mycroft compatibility / adapt translation
    @staticmethod
    def parse_mycroft_skill_intents(path):
        path = expanduser(path)
        if not isinstance(path, str):
            raise ValueError
        if not isdir(path):
            raise NotADirectoryError
        skill_entrypoint = join(path, "__init__.py")
        with open(skill_entrypoint) as _:
            skill = "\n".join(l for l in _.read().split("\n")
                              if not l.strip().startswith("#"))

        # @intent_handler decorator intents
        intents = [i.split("def ")[0].strip().replace("\n", "")
                   for i in skill.split("@intent_handler(")[1:]]
        handlers = [i.split("):")[0].split("def ")[-1].split("(")[0]
                    for i in skill.split("@intent_handler(")[1:]]

        parsed_intents = []
        for idx, intent in enumerate(intents):
            if "IntentBuilder(" not in intent:
                continue
            name = intent.split("IntentBuilder(")[-1].split(")")[0].strip(

            ).rstrip('"').rstrip("'").lstrip('"').lstrip("'")
            kwords = intent.split(")")[1:]
            intent = {
                "engine": "adapt",
                "name": name or handlers[idx],
                "handle": handlers[idx],
                "keywords": []
            }
            for idx, k in enumerate(kwords):
                k = k.replace("\n", "").strip()
                if k.startswith(".require("):
                    k = k.replace(".require(", "").strip().rstrip("'").lstrip(
                        "'").rstrip('"').lstrip('"')
                    intent["keywords"].append(("required", k))
                if k.startswith(".optionally("):
                    k = k.replace(".optionally(", "").strip().rstrip(
                        "'").lstrip("'").rstrip('"').lstrip('"')
                    intent["keywords"].append(("optional", k))
                if k.startswith(".one_of("):
                    k = k.replace(".one_of(", "")[1:-1].strip().split(',')
                    k = [_.strip().rstrip("'").lstrip("'").rstrip('"').lstrip(
                        '"') for _ in k]
                    intent["keywords"].append(("one_of", tuple(k)))
            parsed_intents.append(intent)

        for idx, intent in enumerate(intents):
            if "IntentBuilder(" in intent:
                continue
            name = intent.split(".intent")[0].strip(

            ).rstrip('"').rstrip("'").lstrip('"').lstrip("'")
            intent = {
                "engine": "padatious",
                "handle": handlers[idx],
                "name": name or handlers[idx]
            }
            parsed_intents.append(intent)

        return parsed_intents

    def load_mycroft_skill(self, path, adapt=True, padatious=True):
        skill_name = path.rstrip("/").split("/")[-1]
        self.load_folder(path, lang=self.lang)
        intents = self.parse_mycroft_skill_intents(path)

        # load adapt files
        resources = {}
        for root, folder, files in os.walk(path):
            if self.lang not in root:
                continue
            for f in files:
                if f.endswith(".voc") or f.endswith(".entity"):
                    print(f"INFO: loading entity file {f}")
                    resources[f] = self._load(join(root, f), lang=self.lang,
                                              norm=self._normalize)
                elif f.endswith(".intent"):
                    print(f"INFO: loading intent file {f}")
                    resources[f] = self._load(join(root, f), lang=self.lang,
                                              norm=self._normalize)
                elif f.endswith(".rx"):
                    print(f"WARNING: regex not supported, {f} wont be loaded")

        # generate sample utterances from keywords
        for idx, i in enumerate(intents):
            if i["engine"] == "padatious" and padatious:
                samples = resources.get(i["name"] + ".intent") or []
                i["name"] = i["name"] or f"Intent{idx}(Anonymous)"
                i["name"] = f'{skill_name}:{i["engine"]}:{i["name"]}'
                self.load_intent(i["name"], samples)
            if i["engine"] == "adapt" and adapt:
                samples = self.keywords2samples(i["keywords"], resources)
                i["name"] = i["name"] or f"Intent{idx}(Anonymous)"
                i["name"] = f'{skill_name}:{i["engine"]}:{i["name"]}'
                self.load_intent(i["name"], samples)

    @staticmethod
    def keywords2samples(keywords, resources):
        samples = []
        for kw_type, kw in keywords:
            if kw_type == "required":
                kw_samples = resources.get(kw + ".voc")
                expanded_samples = []
                if not kw_samples:
                    print(f"WARNING: missing {kw}.voc")
                else:
                    for s in list(kw_samples):
                        expanded_samples += expand_options(s)
                if not len(samples):
                    samples = expanded_samples
                else:
                    if not expanded_samples:
                        expanded_samples = ["{ " + kw + " }"]
                    samples = [f"{s} {s2}" for s in samples
                               for s2 in expanded_samples]
            elif kw_type == "optional":
                kw_samples = resources.get(kw + ".voc")
                expanded_samples = []
                if not kw_samples:
                    print(f"WARNING: missing {kw}.voc")
                else:
                    for s in list(kw_samples):
                        expanded_samples += expand_options(s)
                if not len(samples):
                    samples = expanded_samples + ["\n"]
                elif expanded_samples:
                    samples = [f"{s} {s2}" for s in samples
                               for s2 in expanded_samples] + samples
            elif kw_type == "one_of":
                expanded_samples = []
                for kw2 in kw:
                    kw_samples2 = resources.get(kw2 + ".voc") or []
                    if not kw_samples2:
                        print(f"WARNING: missing {kw2}.voc")
                    else:
                        for s in kw_samples2:
                            expanded_samples += expand_options(s)
                if len(samples):
                    samples = [f"{s} {s2}" for s in samples
                               for s2 in expanded_samples]
                else:
                    samples = expanded_samples
        samples = [s.strip() for s in samples]
        samples = list(set(samples))
        return samples

    @staticmethod
    def samples2keywords(samples, lang=None):
        rx_kw = IntentAssistant.samples2regex(samples)
        keywords = []

        # parse required/optional/regex
        kw = {
            "name": "required_kw",
            "required": True,
            "samples": []
        }
        opt_kw = {
            "name": "optional_kw",
            "required": False,
            "samples": []
        }
        for s in samples:
            parsed = expand_keywords(s)
            kw["samples"] += parsed["required"]
            opt_kw["samples"] += parsed["optional"]

        rx = [r for r in kw["samples"] if "{" in r]
        opt_rx = [r for r in opt_kw["samples"] if "{" in r]
        kw["samples"] = list(set([r for r in kw["samples"] if "{" not in r]))
        opt_kw["samples"] = list(
            set([r for r in opt_kw["samples"] if "{" not in r]))

        # segment keywords
        def get_common_kws():
            s2k = {}
            raked = []
            for sample in kw["samples"]:
                # - if rake is installed it will be used, keywords can span
                # multiple tokens
                new_kws = [r[0] for r in segment_keywords(sample, lang=lang)] + \
                          sample.split(" ")
                s2k[sample] = list(set([k for k in new_kws if len(k) > 3]))
                raked += s2k[sample]

            return [k for k in list(set(raked))
                      if all(k in v for v in s2k.values())]

        common = get_common_kws()
        if common:
            # common kwords required by all samples
            for idx, c in enumerate(common):
                c = {
                    "name": f"{c}_ckw{idx}",
                    "required": True,
                    "samples": [c]
                }
                keywords.append(c)

            # one_of kws
            one_of_kws = {}
            parts = []
            for idx, s in enumerate(kw["samples"]):
                if len(common) == 1:
                    pts = s.split(common[0])
                else:
                    import re
                    pattern = f"({'|'.join(common)})"
                    pts = re.split(pattern, s)
                pts = [p.strip() for p in pts if p.strip() and p not in common]

                if pts:
                    parts.append(pts)
            if parts:
                total_parts = max(len(p) for p in parts)
                min_parts = min(len(p) for p in parts)
                for idz in range(0, total_parts - 1):
                    if idz not in one_of_kws:
                        longest = sorted([s[idz] for s in parts], key=len,
                                         reverse=True)
                        name = f"{longest[0].replace(' ', '_')}_pkw{idz}"
                        one_of_kws[idz] = {
                            "name": name,
                            "required": True if idz <= min_parts else False,
                            "samples": [s[idz] for s in parts]
                        }
                    else:
                        one_of_kws[idz]["samples"] += [s[idz] for s in parts]

            for one_of in one_of_kws.values():
                one_of["samples"] = list(set(one_of["samples"]))
                print(one_of)
                keywords.append(one_of)

        else:
            kw["samples"] = [k for k in kw["samples"] if k]
            # create base keyword
            if len(kw["samples"]):
                keywords.append(kw)

        # create base optional keyword
        if len(opt_kw["samples"]):
            keywords.append(opt_kw)

        # regex keywords
        for k, v in rx_kw.items():
            kw_name = "{ " + k.replace("_rx", "") + " }"
            for s in opt_rx:
                if kw_name in s:
                    kw = {
                        "name": k,
                        "required": False,
                        "regex": True,
                        "samples": list(set(rx_kw[k]["samples"]))
                    }
                    if kw not in keywords:
                        keywords.append(kw)

            for s in rx:

                if kw_name in s:
                    kw = {
                        "name": k,
                        "required": True,
                        "regex": True,
                        "samples": list(set(rx_kw[k]["samples"]))
                    }
                    if rx_kw[k]not in keywords:
                        keywords.append(rx_kw[k])

            helpers = []
            for idx, kw in enumerate(list(set(helpers))):
                opt_kw = {
                    "name": "regex_helper_kw_" + str(idx),
                    "required": False,
                    "regex": False,
                    "samples": [kw]
                }
                keywords.append(opt_kw)

        return keywords

    @staticmethod
    def sample2regex(sample):

        kwords = {}

        # expand parentheses into multiple samples
        samples = expand_options(sample)
        # create regex for variables - {some var}

        for s in samples:

            if "{" in s:
                helpers = [h.split("}")[-1] for h in s.split("{")]
                helpers = [h.strip() for h in helpers if h.strip()]

                s = s.replace("[", "(").replace("]", ")")
                rx = list(AutoRegex.get_expressions(s))
                kws = AutoRegex.get_unique_kwords(s)
                for kw in kws:

                    if kw not in kwords:
                        kwords[kw] = {"name": kw + "_rx",
                                      "samples": [],
                                      "required": all(kw in s for s in samples),
                                      "type": "regex"}
                    kwords[kw]["samples"] += rx

                for kw in helpers:
                    if kw not in kwords:
                        kwords[kw] = {"name": kw.replace(" ", "_") +
                                              "_rx_helper",
                                      "samples": [],
                                      "required": False}
                    kwords[kw]["samples"] += [kw]

        return kwords

    @staticmethod
    def samples2regex(samples):
        kwords = {}
        for s in samples:
            merge_dict(kwords, IntentAssistant.sample2regex(s))

        return kwords

    # loading intents
    def load_intent(self, name, samples):
        intent = {name: samples}
        merge_dict(self._intents, intent)

    def load_entity(self, name, samples):
        entity = {name: samples}
        merge_dict(self._entities, entity)

    def load_regex(self, name, samples):
        rx = {name: samples}
        merge_dict(self._regex, rx)

    @staticmethod
    def _load(path, lang="en-us", norm=True, lowercase=True):
        with open(path) as f:
            samples = f.readlines()
        samples = [s.strip() for s in samples if
                   not s.strip().startswith("#")]  # filter comments
        samples = [s.replace("{{", "{").replace("}}", "}") for s in
                   samples]  # clean double brackets
        samples = [s.replace("(", " ( ").replace(")", " ) ")
                       .replace("{", " { ").replace("}", " } ")
                       .replace("|", " | ").replace("]", " ] ")
                       .replace("[", " [ ")
                   for s in samples]  # add missing spaces
        samples = [" ".join(s.split()) for s in
                   samples]  # clean extra white spaces
        if norm:
            samples = [normalize(s, lang, remove_articles=True) for s in
                       samples] + samples
        if lowercase:
            samples = [s.lower() for s in samples if s.lower()]
        return list(set(samples))

    def load_intent_file(self, path):
        path = expanduser(path)
        if not isinstance(path, str):
            raise ValueError
        if isdir(path):
            raise IsADirectoryError
        if not isfile(path):
            raise FileNotFoundError
        if not path.endswith(".intent"):
            print("ERROR: wrong file format {}".format(path))
            if not self.ignore_errors:
                raise ValueError
        name = basename(path).replace(".intent", "")
        samples = self._load(path, lang=self.lang, norm=self._normalize)
        self.load_intent(name, samples)

    def load_entity_file(self, path):
        path = expanduser(path)
        if not isinstance(path, str):
            raise ValueError
        if isdir(path):
            raise IsADirectoryError
        if not isfile(path):
            raise FileNotFoundError
        if not path.endswith(".entity") and not path.endswith(".voc"):
            print("ERROR: wrong file format {}".format(path))
            if not self.ignore_errors:
                raise ValueError
        name = basename(path).replace(".entity", "").replace(".voc", "")
        samples = self._load(path, lang=self.lang, norm=self._normalize)
        self.load_entity(name, samples)

    def load_regex_file(self, path):
        path = expanduser(path)
        if not isinstance(path, str):
            raise ValueError
        if isdir(path):
            raise IsADirectoryError
        if not isfile(path):
            raise FileNotFoundError
        if not path.endswith(".rx"):
            print("ERROR: wrong file format {}".format(path))
            if not self.ignore_errors:
                raise ValueError
        name = basename(path).replace(".rx", "")
        samples = self._load(path, lang=self.lang, norm=False)
        self.load_regex(name, samples)

    def unload_intent(self, name):
        if name not in self._intents:
            raise KeyError
        self._intents.pop(name)

    def unload_entity(self, name):
        if name not in self._entities:
            raise KeyError
        self._entities.pop(name)

    def unload_regex(self, name):
        if name not in self._regex:
            raise KeyError
        self._regex.pop(name)

    # intents formatted for specific engines
    @property
    def adapt_intents(self):
        intents = {}

        for intent_name in self.intents:
            intents[intent_name] = []

            keywords = self.samples2keywords(self.intents[intent_name],
                                             lang=self.lang)
            self.strict = True  # TODO WIP
            if self.strict:
                intent = AdaptBuilder(intent_name)
                for kw in keywords:
                    if kw["required"]:
                        intent.require(kw["name"])
                    else:
                        intent.optionally(kw["name"])
                intents[intent_name] += [{
                    "intent": intent.build().__dict__,
                    "entities": keywords
                }]

            else:
                print("WARNING: strict is an experimental setting, heavy WIP")

                required_kws = [k for k in keywords if
                                k["required"] and not k.get("regex")]
                optional_kws = [k for k in keywords if
                                not k["required"] and not k.get("regex")]

                for k in required_kws:
                    for s in k["samples"]:
                        new_required_keywords = []
                        for t in tokenize(s):
                            if t in self.stop_words:
                                continue
                            kw = {
                                "name": t + "_token",
                                "required": True,
                                "samples": [t]
                            }
                            new_required_keywords.append(kw)

                        intent = AdaptBuilder(intent_name)
                        for kw in new_required_keywords:
                            if kw["required"]:
                                intent.require(kw["name"])
                            else:
                                intent.optionally(kw["name"])
                        intents[intent_name] += [{
                            "intent": intent.build().__dict__,
                            "entities": new_required_keywords + optional_kws
                        }]

        return intents

    @property
    def padaos_intents(self):
        intents = {}

        for intent_name in self.intents:
            samples = []
            ents = []
            for sent in self.intents[intent_name]:
                samples += expand_options(sent)
            for ent in AutoRegex.get_unique_kwords(self.intents[intent_name]):
                if self.entities.get(ent):
                    ents.append({ent: self.entities[ent]})
            intents[intent_name] = [{
                "samples": samples,
                "entities": ents
            }]

        return intents

    @property
    def padatious_intents(self):
        return self.padaos_intents

    @property
    def fuzzy_intents(self):
        intents = {}

        for intent_name in self.intents:
            samples = []
            ents = {}
            for sent in self.intents[intent_name]:
                if "{" in sent:
                    for ent in AutoRegex.get_unique_kwords(
                            self.intents[intent_name]):
                        if ent in self.entities:
                            ents[ent] = self.entities[ent]
                            for valid in self.entities.get(ent, []):
                                samples += [s.replace("{ " + ent + " }", valid)
                                            for s in expand_options(sent)]
                        samples += [s.replace("{ " + ent + " }", "*") for s in
                                    expand_options(sent)]
                else:
                    samples += expand_options(sent)

            intents[intent_name] = [{
                "samples": list(set(samples)),
                "entities": ents
            }]

        return intents

    # testing
    @property
    def expanded_samples(self):
        intents = {}
        for intent in self.fuzzy_intents:
            samples = self.fuzzy_intents[intent][0]["samples"]
            intents[intent] = [s for s in samples if "*" not in s]
        return intents

    @property
    def test_utterances(self):
        intents = {}
        for intent in self.fuzzy_intents:
            samples = self.fuzzy_intents[intent][0]["samples"]
            intents[intent] = {
                "must_match": [s for s in samples if "*" not in s],
                "wildcards": [s for s in samples if "*" in s],
                "auto_generated": []}
        return intents

    @property
    def generated_wildcards(self):
        intents = {}
        for intent in self.expanded_samples:
            samples = self.expanded_samples[intent]
            wild_cards = []
            for s in samples:
                for ent in self.entities:
                    for token in self.entities[ent]:
                        if token in s:
                            wild_cards.append(s.replace(token, "*"))
            intents[intent] = list(set(wild_cards))
        return intents

    # matching
    def match_fuzzy(self, sentence):
        scores = {}
        for intent in self.expanded_samples:
            samples = self.expanded_samples[intent]
            sent, score = match_one(sentence, samples)
            scores[intent] = {"best_match": sent,
                              "conf": score,
                              "intent_name": intent}
        return scores

    def fuzzy_best(self, sentence, min_conf=0.4):
        scores = {}
        best_s = 0
        best_intent = None
        for intent in self.expanded_samples:
            samples = self.expanded_samples[intent]
            sent, score = match_one(sentence, samples)
            scores[intent] = {"best_match": sent, "conf": score,
                              "intent_name": intent}
            if score > best_s:
                best_s = score
                best_intent = intent
        return scores[best_intent] if best_s > min_conf else \
            {"best_match": None, "conf": 0, "intent_name": None}
