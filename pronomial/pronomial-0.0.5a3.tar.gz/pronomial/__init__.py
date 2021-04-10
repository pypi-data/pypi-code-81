from pronomial.utils import predict_gender, pos_tag, word_tokenize, is_plural


class PronomialCoreferenceSolver:
    @staticmethod
    def _load_lang_resources(lang):
        # universal tagset, depends on pos tagger model for each lang
        PRONOUN_TAG = ['PRON']
        NOUN_TAG = ['NOUN']
        JJ_TAG = ['ADJ']
        PLURAL_NOUN_TAG = ['NOUN']
        SUBJ_TAG = ['NOUN']

        # this is a basic mechanism to allow to "look back", the naming
        # reflects what this does poorly, each language can define word
        # pairs that will give preference to an earlier noun in the
        # sentence, loosely named after a couple examples in the
        # english unittests. TODO generalize this
        WITH = WITH_FOLLOWUP = THAT = THAT_FOLLOWUP = IN = IN_FOLLOWUP = []

        NEUTRAL_WORDS = []

        # tokens that indicate the verb_subject should be selected
        SUBJ_INDICATORS = []

        # symbol used when merging Nouns to replace plural pronouns
        NAME_JOINER = "+"

        # word lists
        PRONOUNS = {}
        GENDERED_WORDS = {}

        # Load resources for selected lang
        if lang.startswith("en"):
            from pronomial.lang.en import NOUN_TAG_EN, PLURAL_NOUN_TAG_EN, \
                PRONOUNS_EN, PRONOUN_TAG_EN, SUBJ_TAG_EN, JJ_TAG_EN, WITH_EN, \
                GENDERED_WORDS_EN, WITH_FOLLOWUP_EN, THAT_EN, \
                THAT_FOLLOWUP_EN, NEUTRAL_WORDS_EN, SUBJ_INDICATORS_EN, \
                NAME_JOINER_EN, IN_EN, IN_FOLLOWUP_EN
            GENDERED_WORDS = GENDERED_WORDS_EN
            NOUN_TAG = NOUN_TAG_EN
            SUBJ_TAG = SUBJ_TAG_EN
            PRONOUN_TAG = PRONOUN_TAG_EN
            PRONOUNS = PRONOUNS_EN
            PLURAL_NOUN_TAG = PLURAL_NOUN_TAG_EN
            JJ_TAG = JJ_TAG_EN
            WITH = WITH_EN
            WITH_FOLLOWUP = WITH_FOLLOWUP_EN
            THAT = THAT_EN
            THAT_FOLLOWUP = THAT_FOLLOWUP_EN
            NEUTRAL_WORDS = NEUTRAL_WORDS_EN
            SUBJ_INDICATORS = SUBJ_INDICATORS_EN
            NAME_JOINER = NAME_JOINER_EN
            IN = IN_EN
            IN_FOLLOWUP = IN_FOLLOWUP_EN
        elif lang.startswith("pt"):
            from pronomial.lang.pt import PRONOUNS_PT, GENDERED_WORDS_PT
            GENDERED_WORDS = GENDERED_WORDS_PT
            PRONOUNS = PRONOUNS_PT
        elif lang.startswith("es"):
            from pronomial.lang.es import PRONOUNS_ES, GENDERED_WORDS_ES
            GENDERED_WORDS = GENDERED_WORDS_ES
            PRONOUNS = PRONOUNS_ES
        elif lang.startswith("ca"):
            from pronomial.lang.ca import PRONOUNS_CA, GENDERED_WORDS_CA
            GENDERED_WORDS = GENDERED_WORDS_CA
            PRONOUNS = PRONOUNS_CA

        return PRONOUN_TAG, NOUN_TAG, JJ_TAG, PLURAL_NOUN_TAG, SUBJ_TAG, \
               WITH, WITH_FOLLOWUP, THAT, THAT_FOLLOWUP, IN, IN_FOLLOWUP, \
               NEUTRAL_WORDS, SUBJ_INDICATORS, NAME_JOINER, PRONOUNS, \
               GENDERED_WORDS

    @staticmethod
    def detect_nouns(sentence, lang="en", return_idx=True):

        PRONOUN_TAG, NOUN_TAG, JJ_TAG, PLURAL_NOUN_TAG, SUBJ_TAG, \
        WITH, WITH_FOLLOWUP, THAT, THAT_FOLLOWUP, IN, IN_FOLLOWUP, \
        NEUTRAL_WORDS, SUBJ_INDICATORS, NAME_JOINER, PRONOUNS, \
        GENDERED_WORDS = PronomialCoreferenceSolver._load_lang_resources(lang)

        tags = pos_tag(sentence, lang=lang)
        prev_names_idx = {
            "male": [],
            "female": [],
            "first": [],
            "neutral": [],
            "plural": [],
            "subject": [],
            "verb_subject": []
        }

        for idx, (w, t) in enumerate(tags):
            next_w, next_t = tags[idx + 1] if idx < len(tags) - 1 else ("", "")
            prev_w, prev_t = tags[idx - 1] if idx > 0 else ("", "")
            if t in NOUN_TAG:
                if prev_w in NEUTRAL_WORDS:
                    prev_names_idx["neutral"].append(idx)
                else:
                    gender = predict_gender(w, prev_w, lang=lang)
                    if w in PRONOUNS["female"] or \
                            w.lower() in GENDERED_WORDS["female"]:
                        prev_names_idx["female"].append(idx)
                    elif w in PRONOUNS["male"] or \
                            w.lower() in GENDERED_WORDS["male"]:
                        prev_names_idx["male"].append(idx)
                    elif w[0].isupper() or prev_t in ["DET"]:
                        prev_names_idx[gender].append(idx)
                    prev_names_idx["subject"].append(idx)
                    prev_names_idx["neutral"].append(idx)

                if next_t.startswith("V") and not prev_t.startswith("V"):
                    prev_names_idx["verb_subject"].append(idx)

            elif t in SUBJ_TAG:
                prev_names_idx["subject"].append(idx)
                gender = predict_gender(w, prev_w, lang=lang)
                prev_names_idx["neutral"].append(idx)
                if gender == "female":
                    prev_names_idx["female"].append(idx)
                if gender == "male":
                    prev_names_idx["male"].append(idx)
            elif t in PLURAL_NOUN_TAG:
                prev_names_idx["plural"].append(idx)
                if w[0].isupper():
                    gender = predict_gender(w, prev_w, lang=lang)
                    if not prev_names_idx[gender]:
                        prev_names_idx[gender].append(idx)
            elif t in JJ_TAG:  # common tagger error
                if w[0].isupper():
                    gender = predict_gender(w, prev_w, lang=lang)
                    if not prev_names_idx[gender]:
                        prev_names_idx[gender].append(idx)
                if not prev_names_idx["neutral"]:
                    prev_names_idx["neutral"].append(idx)
                if not prev_names_idx["subject"]:
                    prev_names_idx["subject"].append(idx)

        if isinstance(sentence, str):
            tokens = word_tokenize(sentence)
        else:
            tokens = sentence

        if not return_idx:
            prev_names_idx = {k: [tokens[i] for i in v]
                              for k, v in prev_names_idx.items()}
        prev_names_idx["tokens"] = tokens
        return prev_names_idx

    @staticmethod
    def solve_corefs(sentence, lang="en"):
        PRONOUN_TAG, NOUN_TAG, JJ_TAG, PLURAL_NOUN_TAG, SUBJ_TAG, \
        WITH, WITH_FOLLOWUP, THAT, THAT_FOLLOWUP, IN, IN_FOLLOWUP, \
        NEUTRAL_WORDS, SUBJ_INDICATORS, NAME_JOINER, PRONOUNS, \
        GENDERED_WORDS = PronomialCoreferenceSolver._load_lang_resources(lang)

        tags = pos_tag(sentence, lang=lang)
        pron_list = [p for k, p in PRONOUNS.items()]
        flatten = lambda l: [item for sublist in l for item in sublist]
        pron_list = flatten(pron_list)

        tagged_nouns = PronomialCoreferenceSolver.detect_nouns(sentence, lang)
        tokens = tagged_nouns.pop("tokens")
        candidates = []

        for idx, (w, t) in enumerate(tags):
            if (t in PRONOUN_TAG and w.lower() in pron_list) or \
                    any(w in items for k, items in PRONOUNS.items()):
                prev_w, prev_t = tags[idx - 1] if idx > 0 else ("", "")
                prev_names = {k: [tokens[i] for i in v if i <= idx]
                              for k, v in tagged_nouns.items()}
                # this is a basic mechanism to allow to "look back", the naming
                # reflects what this does poorly, each language can define word
                # pairs that will give preference to an earlier noun in the
                # sentence, loosely named after a couple examples in the
                # english unittests. TODO generalize this
                idz = -1
                if prev_w.lower() in WITH and w.lower() in WITH_FOLLOWUP:
                    idz = -2
                elif prev_w.lower() in THAT and w.lower() in THAT_FOLLOWUP:
                    idz = -2
                elif prev_w.lower() in IN and w.lower() in IN_FOLLOWUP:
                    idz = -2
                wl = w.lower()
                if wl in PRONOUNS["male"]:
                    # give preference to verb subjects
                    n = prev_names["male"]
                    if (wl in SUBJ_INDICATORS or prev_w in SUBJ_INDICATORS) \
                            and prev_names["verb_subject"]:
                        n = [_ for _ in prev_names["male"]
                             if _ in prev_names["verb_subject"]] or n
                    if n:
                        if abs(idz) > len(n):
                            idz = 0
                        candidates.append((idx, w, n[idz]))
                    elif prev_names["subject"]:
                        if abs(idz) > len(prev_names["subject"]):
                            idz = 0
                        candidates.append((idx, w, prev_names["subject"][idz]))
                elif wl in PRONOUNS["female"]:
                    # give preference to verb subjects
                    n = prev_names["female"]
                    if (wl in SUBJ_INDICATORS or prev_w in SUBJ_INDICATORS) \
                            and prev_names["verb_subject"]:
                        n = [_ for _ in prev_names["female"]
                             if _ in prev_names["verb_subject"]] or n
                    if n:
                        if abs(idz) > len(n):
                            idz = 0
                        candidates.append((idx, w, n[idz]))
                    elif prev_names["subject"]:
                        if abs(idz) > len(prev_names["subject"]):
                            idz = 0
                        candidates.append((idx, w, prev_names["subject"][idz]))
                elif wl in PRONOUNS["neutral"]:
                    # give preference to verb subjects
                    n = prev_names["neutral"]
                    if prev_names["verb_subject"]:
                        n = [_ for _ in prev_names["neutral"]
                             if _ in prev_names["verb_subject"]] or n
                    if n:
                        if abs(idz) > len(n):
                            idz = 0
                        candidates.append((idx, w, n[idz]))
                    elif prev_names["subject"]:
                        if abs(idz) > len(prev_names["subject"]):
                            idz = 0
                        candidates.append((idx, w, prev_names["subject"][idz]))
                elif wl in PRONOUNS["plural"]:
                    plural_subjs = [_ for _ in prev_names["subject"] if
                                    is_plural(_, lang)]
                    names = prev_names["male"] + prev_names["female"]
                    if prev_names["plural"]:
                        if abs(idz) > len(prev_names["plural"]):
                            idz = 0
                        candidates.append((idx, w, prev_names["plural"][idz]))
                    elif plural_subjs:
                        if abs(idz) > len(plural_subjs):
                            idz = 0
                        candidates.append((idx, w, plural_subjs[idz]))
                    elif t in ["WP"] and prev_names["subject"]:
                        if abs(idz) > len(prev_names["subject"]):
                            idz = 0
                        candidates.append((idx, w, prev_names["subject"][idz]))
                    elif len(names) == 2:
                        merged_names = NAME_JOINER.join([_ for _ in names if
                                                         _[0].isupper()])
                        candidates.append((idx, w, merged_names))
                else:
                    for k, v in PRONOUNS.items():
                        if prev_names[k] and wl in v:
                            if abs(idz) > len(prev_names[k]):
                                idz = 0
                            candidates.append((idx, w, prev_names[k][idz]))
                    else:
                        if prev_names["subject"] and \
                                wl not in PRONOUNS["first"]:
                            if abs(idz) > len(prev_names["subject"]):
                                idz = 0
                            candidates.append(
                                (idx, w, prev_names["subject"][idz]))
        return candidates

    @staticmethod
    def score_corefs(sentence, lang="en"):
        PRONOUN_TAG, NOUN_TAG, JJ_TAG, PLURAL_NOUN_TAG, SUBJ_TAG, \
        WITH, WITH_FOLLOWUP, THAT, THAT_FOLLOWUP, IN, IN_FOLLOWUP, \
        NEUTRAL_WORDS, SUBJ_INDICATORS, NAME_JOINER, PRONOUNS, \
        GENDERED_WORDS = PronomialCoreferenceSolver._load_lang_resources(lang)

        tags = pos_tag(sentence, lang=lang)
        pron_list = [p for k, p in PRONOUNS.items()]
        flatten = lambda l: [item for sublist in l for item in sublist]
        pron_list = flatten(pron_list)

        tagged_nouns = PronomialCoreferenceSolver.detect_nouns(sentence, lang)
        tokens = tagged_nouns.pop("tokens")
        candidates = {}

        for idx, (w, t) in enumerate(tags):
            if (t in PRONOUN_TAG and w.lower() in pron_list) or \
                    any(w in items for k, items in PRONOUNS.items()):
                candidates[idx] = {}

                prev_w, prev_t = tags[idx - 1] if idx > 0 else ("", "")
                prev_ids = {k: [i for i in v if i <= idx]
                            for k, v in tagged_nouns.items()}
                prev_names = {k: [tokens[i] for i in v]
                              for k, v in prev_ids.items()}
                # this is a basic mechanism to allow to "look back", the naming
                # reflects what this does poorly, each language can define word
                # pairs that will give preference to an earlier noun in the
                # sentence, loosely named after a couple examples in the
                # english unittests. TODO generalize this
                idz = -1
                if prev_w.lower() in WITH and w.lower() in WITH_FOLLOWUP:
                    idz = -2
                elif prev_w.lower() in THAT and w.lower() in THAT_FOLLOWUP:
                    idz = -2
                elif prev_w.lower() in IN and w.lower() in IN_FOLLOWUP:
                    idz = -2
                wl = w.lower()

                if wl in PRONOUNS["male"]:
                    # give preference to verb subjects
                    s = []
                    if (wl in SUBJ_INDICATORS or prev_w in SUBJ_INDICATORS) \
                            and prev_names["verb_subject"]:
                        s = [_ for _ in prev_names["male"]
                             if _ in prev_names["verb_subject"]]

                    if prev_names["male"]:
                        if abs(idz) > len(prev_names["male"]):
                            idz = 0
                        for ids, x in enumerate(prev_ids["male"]):
                            if x not in candidates[idx]:
                                candidates[idx][x] = 0
                            candidates[idx][x] += 10  # gender match
                            # freshness bonus
                            candidates[idx][x] += ids
                            if ids == idz:
                                candidates[idx][x] += 10
                            if tokens[x] in s:
                                candidates[idx][x] += 10  # verb subject match

                    if prev_names["subject"]:
                        if abs(idz) > len(prev_names["subject"]):
                            idz = 0
                        for ids, x in enumerate(prev_ids["subject"]):
                            if x not in candidates[idx]:
                                candidates[idx][x] = 0
                            if ids == idz:
                                candidates[idx][x] += 10  # freshness bonus
                            candidates[idx][x] += ids

                elif wl in PRONOUNS["female"]:
                    # give preference to verb subjects
                    s = []
                    if (wl in SUBJ_INDICATORS or prev_w in SUBJ_INDICATORS) \
                            and prev_names["verb_subject"]:
                        s = [_ for _ in prev_names["female"]
                             if _ in prev_names["verb_subject"]]

                    if prev_names["female"]:
                        if abs(idz) > len(prev_names["female"]):
                            idz = 0
                        for ids, x in enumerate(prev_ids["female"]):
                            if x not in candidates[idx]:
                                candidates[idx][x] = 0

                            candidates[idx][x] += 10  # gender match
                            # freshness bonus
                            candidates[idx][x] += ids
                            if ids == idz:
                                candidates[idx][x] += 10
                            if tokens[x] in s:
                                candidates[idx][x] += 10  # verb subject match

                    if prev_names["subject"]:
                        if abs(idz) > len(prev_names["subject"]):
                            idz = 0
                        for ids, x in enumerate(prev_ids["subject"]):
                            if x not in candidates[idx]:
                                candidates[idx][x] = 0
                            if ids == idz:
                                candidates[idx][x] += 10  # freshness bonus
                            candidates[idx][x] += ids

        """                     
             elif wl in PRONOUNS["neutral"]:
                 # give preference to verb subjects
                 n = prev_names["neutral"]
                 if prev_names["verb_subject"]:
                     n = [_ for _ in prev_names["neutral"]
                          if _ in prev_names["verb_subject"]] or n
                 if n:
                     if abs(idz) > len(n):
                         idz = 0
                     candidates.append((idx, w, n[idz]))
                 elif prev_names["subject"]:
                     if abs(idz) > len(prev_names["subject"]):
                         idz = 0
                     candidates.append((idx, w, prev_names["subject"][idz]))
             elif wl in PRONOUNS["plural"]:
                 plural_subjs = [_ for _ in prev_names["subject"] if
                                 is_plural(_, lang)]
                 names = prev_names["male"] + prev_names["female"]
                 if prev_names["plural"]:
                     if abs(idz) > len(prev_names["plural"]):
                         idz = 0
                     candidates.append((idx, w, prev_names["plural"][idz]))
                 elif plural_subjs:
                     if abs(idz) > len(plural_subjs):
                         idz = 0
                     candidates.append((idx, w, plural_subjs[idz]))
                 elif t in ["WP"] and prev_names["subject"]:
                     if abs(idz) > len(prev_names["subject"]):
                         idz = 0
                     candidates.append((idx, w, prev_names["subject"][idz]))
                 elif len(names) == 2:
                     merged_names = NAME_JOINER.join([_ for _ in names if
                                                      _[0].isupper()])
                     candidates.append((idx, w, merged_names))
             else:
                 for k, v in PRONOUNS.items():
                     if prev_names[k] and wl in v:
                         if abs(idz) > len(prev_names[k]):
                             idz = 0
                         candidates.append((idx, w, prev_names[k][idz]))
                 else:
                     if prev_names["subject"] and \
                             wl not in PRONOUNS["first"]:
                         if abs(idz) > len(prev_names["subject"]):
                             idz = 0
                         candidates.append(
                             (idx, w, prev_names["subject"][idz]))
        """

        # make score of all results add up to 1
        for tok_idx in candidates:
            total = sum(
                score for tok2_idx, score in candidates[tok_idx].items())
            for tok2_idx, score in candidates[tok_idx].items():
                candidates[tok_idx][tok2_idx] = score / total
        return candidates

    @classmethod
    def replace_corefs(cls, text, lang="en"):
        tokens = word_tokenize(text)
        for idx, _, w in cls.solve_corefs(text, lang=lang):
            tokens[idx] = w
        return " ".join(tokens)

    @staticmethod
    def normalize(text):
        return " ".join(word_tokenize(text))


def normalize(text):
    return PronomialCoreferenceSolver.normalize(text)


def detect_nouns(text, lang="en", return_idx=True):
    return PronomialCoreferenceSolver.detect_nouns(text, lang=lang,
                                                   return_idx=return_idx)


def link_pronouns(text, lang="en"):
    return PronomialCoreferenceSolver.solve_corefs(text, lang=lang)


def score_corefs(text, lang="en"):
    return PronomialCoreferenceSolver.score_corefs(text, lang=lang)


def replace_corefs(text, lang="en"):
    return PronomialCoreferenceSolver.replace_corefs(text, lang=lang)
