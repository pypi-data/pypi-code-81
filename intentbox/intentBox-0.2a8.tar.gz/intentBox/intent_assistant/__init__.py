from os.path import expanduser, isdir, isfile, join, basename
import os

from adapt.intent import IntentBuilder as AdaptBuilder
from auto_regex import AutoRegex

from intentBox.lang.en import ENGLISH_STOP_WORDS
from intentBox.lang.pt import PORTUGUESE_STOP_WORDS
from intentBox.lang import GENERIC_STOP_WORDS
from intentBox.segmentation import get_common_chunks, rake, chunk
from intentBox.utils import tokenize, normalize, expand_options, \
    expand_keywords, merge_dict, match_one, flatten


def keyword_start_split(samples):
    samples = [expand_options(s) for s in samples]
    samples = flatten(samples)
    keywords = []
    samples = [k for k in samples if k]
    # detect shared utterance starts + split into own keyword
    starts = {}
    if len(samples) > 1:
        for i in range(3):
            st = list(set([" ".join(k.split(" ")[:3 - i])
                           for k in samples if k]))
            counts = {s: len([_ for _ in samples
                              if _.startswith(s)]) / len(samples)
                      for s in st}
            if counts and all(v >= 0.35 for v in counts.values()) and \
                    not any(c in samples for c in counts.keys()):
                starts = counts
                break

    if starts:
        keywords.append({
            "name": "start_kw",
            "required": True,
            "samples": list(starts.keys())
        })
        # update samples to remove starts
        for idx, s in enumerate(samples):
            for k in starts:
                if s.startswith(k):
                    samples[idx] = s[len(k):].strip()

    # create base keyword
    if len(samples):
        keywords.append({
            "name": "required_kw",
            "required": True,
            "samples": list(set(samples))
        })

    return keywords


def keyword_end_split(samples):
    samples = [expand_options(s) for s in samples]
    samples = flatten(samples)
    keywords = []
    samples = [k for k in samples if k]
    # detect shared utterance starts + split into own keyword
    ends = {}
    if len(samples) > 1:
        for i in range(3):
            st = list(set([" ".join(k.split(" ")[-(3 - i):])
                           for k in samples if k]))
            counts = {s: len([_ for _ in samples
                              if _.endswith(s)]) / len(samples)
                      for s in st}
            if counts and all(v >= 0.35 for v in counts.values()) and \
                    not any(c in samples for c in counts.keys()):
                ends = counts
                break

    if ends:
        keywords.append({
            "name": "end_kw",
            "required": True,
            "samples": [" ".join([_ for _ in s.split(" ") if len(_) > 2])
                        for s in ends.keys()]
        })
        # update samples to remove ends
        for idx, s in enumerate(samples):
            for k in ends:
                if s.endswith(k):
                    samples[idx] = s[:-len(k)].strip()

    # create base keyword
    if len(samples):
        keywords.insert(0, {
            "name": "required_kw",
            "required": True,
            "samples": list(set(samples))
        })

    return keywords


def keyword_entity_split(samples, lang="en-us"):
    keywords = []
    try:
        kws = [rake(s, lang=lang)[0][0] for s in samples]
    except IndexError:
        kws = []

    kws = list(set([k for k in kws if all(k in s for s in samples)]))

    if not kws:
        kws = get_common_chunks(samples, lang)
        kws = list(set([k for k in kws if all(k in s for s in samples)]))
        if len(kws) > 1:
            kws = [sorted(kws, key=len, reverse=True)[0]]

    if kws:
        keywords += [{
            "name": f"entity_kw_{kws[0]}".replace(" ", "_"),
            "required": True,
            "samples": kws
        }]
        qs = []
        hs = []
        chunked = [chunk(s, delimiters=kws) for s in samples]
        for ch in chunked:
            ch = [c for c in ch if c not in kws and len(c) > 1]
            if lang.startswith("en"):
                if "ing" in ch:
                    kws += [k + "ing" for k in kws if not k.endswith("ing")]
                ch = [c for c in ch if c not in ["ing", "'s", "s"]]
            if len(ch) == 1:
                qs += ch
            elif len(ch) == 2:
                qs += [ch[0]]
                hs += [ch[1]]

        qs = [q for q in qs if q not in kws]
        hs = [q for q in hs if q not in kws]
        if qs:
            keywords += [{
                "name": "start_chunk_kw",
                "required": True,
                "samples": list(set(qs))
            }]
        if hs:
            min_ = min(len(ch) for ch in chunked)
            max_ = max(len(ch) for ch in chunked)
            keywords += [{
                "name": "end_chunk_kw",
                "required": min_ == max_,
                "samples": list(set(hs))
            }]

    return keywords or [{
        "name": "required_kw",
        "required": True,
        "samples": samples
    }]


def keyword_split(samples, lang="en-us"):
    samples = [expand_options(s) for s in samples]
    samples = flatten(samples)
    keywords = keyword_start_split(samples)
    # start keyword detected
    if len(keywords) == 2:
        return keywords
    # fallback to main entity keyword split
    keywords = keyword_end_split(samples)
    if len(keywords) == 2:
        return keywords
    return keyword_entity_split(samples, lang)


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
    def samples2keywords(samples, lang="en-us"):
        keywords = []

        # expand samples
        samples = [expand_options(s) for s in samples]
        samples = flatten(samples)

        # parse required/optional
        kw_samples = []
        opt_kw = []
        for s in samples:
            parsed = expand_keywords(s)
            kw_samples += parsed["required"]
            opt_kw += parsed["optional"]

        kw_samples = list(set([r for r in kw_samples if "{" not in r]))
        opt_kw = list(set([r for r in opt_kw if "{" not in r]))

        # create base optional keyword
        if len(opt_kw):
            keywords.append({
                "name": "optional_kw",
                "required": False,
                "samples": opt_kw
            })

        # segment keywords
        keywords += keyword_split(kw_samples, lang=lang)

        # extract required samples for reference/deduplication
        rs = flatten([k["samples"] for k in keywords if k["required"]])

        # regex keywords
        rx_kw = IntentAssistant.samples2regex(samples)

        # TODO autoregex has a bug where _ in names are removed
        # this causes kw extraction in IntentAssistant.samples2regex to be
        # incorrect
        rx = flatten([chunk(_, ["{"]) for _ in samples if "{" in _])
        rx = list(set([_.split("}")[0].strip()
                       for _ in rx if "}" in _]))
        kmap = {k.replace("_", ""): k for k in rx}
        # END TODO

        for k, v in rx_kw.items():
            if v.get("type", "") == "regex":
                # if kw in all samples -> required
                required = all("{ " + kmap[k] + " }" in s
                               or "{" + kmap[k] + "}" in s
                               for s in samples)

                # add regex keyword
                keywords.append({
                    "name": v["name"],
                    "entity": k,
                    "required": required,
                    "regex": True,
                    "samples": list(set(v["samples"]))
                })

                # use non regex chunks as helper_kws
                s = [chunk(_, ["{ " + kmap[k] + " }", "{" + kmap[k] + "}"])
                     for _ in samples]
                s = flatten([[x for x in _ if "{" not in x] for _ in s])
                s = list(set([" ".join([x for x in _.split(" ") if len(x) > 2])
                              for _ in s]))

                # filter samples already in required_kw
                reqs = [_ for _ in s if
                        all(_ in s for s in samples) and _.strip()
                        and _ not in rs]
                opts = [_ for _ in s if _ not in reqs and _.strip()
                        and _ not in rs]

                # create helper keywords to boost regex matches
                if len(reqs):
                    keywords.append({
                        "name": k + "_rx_helper",
                        "required": True,
                        "samples": list(set(reqs))
                    })
                if len(opts):
                    keywords.append({
                        "name": k + "_optional_rx_helper",
                        "required": False,
                        "samples": list(set(opts))
                    })

        return [k for k in keywords if k["samples"]]

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
                                      "required": all(
                                          kw in s for s in samples),
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
