from pronomial.utils import predict_gender, pos_tag, word_tokenize


class PronomialCoreferenceSolver:
    @staticmethod
    def solve_corefs(sentence, lang="en"):
        # universal tagset, langs can override these depending on pos tagger
        # model
        PRONOUN_TAG = ['PRON']
        NOUN_TAG = ['NOUN']
        JJ_TAG = ['ADJ']
        PLURAL_NOUN_TAG = ['NOUN']
        SUBJ_TAG = ['NOUN']
        WITH = WITH_FOLLOWUP = THAT = THAT_FOLLOWUP = []
        NEUTRAL_WORDS = []

        if lang.startswith("en"):
            from pronomial.lang.en import NOUN_TAG_EN, PLURAL_NOUN_TAG_EN, \
                PRONOUNS_EN, PRONOUN_TAG_EN, SUBJ_TAG_EN, JJ_TAG_EN, WITH_EN,\
                GENDERED_WORDS_EN, WITH_FOLLOWUP_EN, THAT_EN, \
                THAT_FOLLOWUP_EN, NEUTRAL_WORDS_EN
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
        else:
            raise NotImplementedError

        tags = pos_tag(sentence, lang=lang)
        pron_list = [p for k, p in PRONOUNS.items()]
        flatten = lambda l: [item for sublist in l for item in sublist]
        pron_list = flatten(pron_list)

        prev_names = {
            "male": [],
            "female": [],
            "first": [],
            "neutral": [],
            "plural": [],
            "subject": [],
            "verb_subject": []
        }
        candidates = []

        for idx, (w, t) in enumerate(tags):
            next_w, next_t = tags[idx + 1] if idx < len(tags) - 1 else ("", "")
            prev_w, prev_t = tags[idx - 1] if idx > 0 else ("", "")
            idz = -1
            if prev_w.lower() in WITH and w.lower() in WITH_FOLLOWUP:
                idz = -2
            elif prev_w.lower() in THAT and w.lower() in THAT_FOLLOWUP:
                idz = -2

            if t in NOUN_TAG:
                if prev_w in NEUTRAL_WORDS:
                    prev_names["neutral"].append(w)
                else:
                    gender = predict_gender(w, prev_w, lang=lang)
                    if w in PRONOUNS["female"] or\
                            w.lower() in GENDERED_WORDS["female"]:
                        prev_names["female"].append(w)
                    elif w in PRONOUNS["male"] or \
                            w.lower() in GENDERED_WORDS["male"]:
                        prev_names["male"].append(w)
                    elif w[0].isupper() or prev_t in ["DET"]:
                        prev_names[gender].append(w)
                    prev_names["neutral"].append(w)
                    prev_names["subject"].append(w)

                    if next_t.startswith("V"):
                        prev_names["verb_subject"] = w

            elif t in SUBJ_TAG:
                prev_names["subject"].append(w)
                gender = predict_gender(w, prev_w, lang=lang)
                prev_names["neutral"].append(w)
                if gender == "female":
                    prev_names["female"].append(w)
                if gender == "male":
                    prev_names["male"].append(w)
            elif (t in PRONOUN_TAG and w.lower() in pron_list) or any(w in items
                                         for k, items in PRONOUNS.items()):
                w = w.lower()
                if w in PRONOUNS["male"]:
                    if prev_names["male"]:
                        candidates.append((idx, w, prev_names["male"][idz]))
                    elif prev_names["subject"]:
                        candidates.append((idx, w, prev_names["subject"][idz]))
                elif w in PRONOUNS["female"]:
                    if prev_names["female"]:
                        candidates.append((idx, w, prev_names["female"][idz]))
                    elif prev_names["subject"]:
                        candidates.append((idx, w, prev_names["subject"][idz]))
                elif w in PRONOUNS["neutral"]:
                    # give preference to verb subjects
                    n = prev_names["neutral"]
                    if prev_names["verb_subject"]:
                        n = [_ for _ in prev_names["neutral"]
                             if _ in prev_names["verb_subject"]] or n
                    if n:
                        candidates.append((idx, w, n[idz]))
                    elif prev_names["subject"]:
                        candidates.append((idx, w, prev_names["subject"][idz]))
                else:
                    if w in PRONOUNS["plural"] and prev_names["plural"]:
                        candidates.append((idx, w, prev_names["plural"][idz]))
                    elif w in PRONOUNS["first"] and prev_names["first"]:
                        candidates.append((idx, w, prev_names["first"][idz]))
                    elif w in PRONOUNS["plural"] and prev_names["subject"]:
                        candidates.append((idx, w, prev_names["subject"][idz]))
                    else:
                        for k, v in PRONOUNS.items():
                            if prev_names[k] and w in v:
                                candidates.append((idx, w, prev_names[k][idz]))
                        else:
                            if prev_names["subject"] and \
                                    w not in PRONOUNS["first"]:
                                candidates.append(
                                    (idx, w, prev_names["subject"][idz]))
            elif t in PLURAL_NOUN_TAG:
                prev_names["plural"].append(w)
                if w[0].isupper():
                    gender = predict_gender(w, prev_w, lang=lang)
                    if not prev_names[gender]:
                        prev_names[gender].append(w)
            elif t in JJ_TAG:  # common tagger error
                if w[0].isupper():
                    gender = predict_gender(w, prev_w, lang=lang)
                    if not prev_names[gender]:
                        prev_names[gender].append(w)
                if not prev_names["neutral"]:
                    prev_names["neutral"].append(w)
                if not prev_names["subject"]:
                    prev_names["subject"].append(w)
        return candidates

    @classmethod
    def replace_corefs(cls, text, lang="en"):
        tokens=word_tokenize(text)
        for idx, _, w in cls.solve_corefs(text, lang=lang):
            tokens[idx] = w
        return " ".join(tokens)


def replace_corefs(text, lang="en"):
    return PronomialCoreferenceSolver.replace_corefs(text, lang=lang)
