from pronomial.utils import predict_gender, pos_tag, word_tokenize


class PronomialCoreferenceSolver:
    @staticmethod
    def solve_corefs(sentence, lang="en"):
        if lang.startswith("en"):
            from pronomial.lang.en import NOUN_TAG_EN, PLURAL_NOUN_TAG_EN, \
                CATEGORY_EN, PRONOUN_TAG_EN, SUBJ_TAG_EN, JJ_TAG_EN, GENDERED_WORDS_EN
            NOUN_TAG = NOUN_TAG_EN
            SUBJ_TAG = SUBJ_TAG_EN
            PRONOUN_TAG = PRONOUN_TAG_EN
            CATEGORY = CATEGORY_EN
            PLURAL_NOUN_TAG = PLURAL_NOUN_TAG_EN
            JJ_TAG = JJ_TAG_EN
            GENDERED_WORDS = GENDERED_WORDS_EN
        elif lang.startswith("pt"):
            from pronomial.lang.pt import NOUN_TAG_PT, PLURAL_NOUN_TAG_PT, \
                PRONOUN_TAG_PT, SUBJ_TAG_PT, JJ_TAG_PT, CATEGORY_PT, \
                GENDERED_WORDS_PT
            NOUN_TAG = NOUN_TAG_PT
            GENDERED_WORDS = GENDERED_WORDS_PT
            SUBJ_TAG = SUBJ_TAG_PT
            PRONOUN_TAG = PRONOUN_TAG_PT
            CATEGORY = CATEGORY_PT
            PLURAL_NOUN_TAG = PLURAL_NOUN_TAG_PT
            JJ_TAG = JJ_TAG_PT
        else:
            raise NotImplementedError

        tags = pos_tag(sentence, lang=lang)

        prev_names = {
            "male": [],
            "female": [],
            "first": [],
            "neutral": [],
            "plural": [],
            "subject": [],
            "subject_gender": "neutral"
        }
        candidates = []

        for idx, (w, t) in enumerate(tags):
            next_w, next_t = tags[idx + 1] if idx < len(tags) - 1 else ("", "")
            prev_w, prev_t = tags[idx - 1] if idx > 0 else ("", "")
            if t in NOUN_TAG:
                gender = predict_gender(w, prev_w, lang=lang)
                if w in CATEGORY["female"] or\
                        w.lower() in GENDERED_WORDS["female"]:
                    prev_names["female"].append(w)
                elif w in CATEGORY["male"] or \
                        w.lower() in GENDERED_WORDS["male"]:
                    prev_names["male"].append(w)
                elif w[0].isupper() or prev_t in ["DET"]:
                    prev_names[gender].append(w)
                prev_names["neutral"].append(w)
                prev_names["subject"].append(w)
                prev_names["subject_gender"] = gender
            elif t in SUBJ_TAG:
                prev_names["subject"].append(w)
                gender = predict_gender(w, prev_w, lang=lang)
                prev_names["subject_gender"] = gender
                prev_names["neutral"].append(w)
                if gender == "female":
                    prev_names["female"].append(w)
                if gender == "male":
                    prev_names["male"].append(w)
            elif t in PRONOUN_TAG or any(w in items
                                         for k, items in CATEGORY.items()):
                w = w.lower()
                if w in CATEGORY["male"]:
                    if prev_names["male"]:
                        candidates.append((idx, w, prev_names["male"][-1]))
                    elif prev_names["subject"]:
                        candidates.append((idx, w, prev_names["subject"][-1]))
                elif w in CATEGORY["female"]:
                    if prev_names["female"]:
                        candidates.append((idx, w, prev_names["female"][-1]))
                    elif prev_names["subject"]:
                        candidates.append((idx, w, prev_names["subject"][-1]))
                elif w in CATEGORY["neutral"]:
                    if prev_names["neutral"]:
                        candidates.append((idx, w, prev_names["neutral"][0]))
                    elif prev_names["subject"]:
                        candidates.append((idx, w, prev_names["subject"][-1]))
                else:
                    if w in CATEGORY["plural"] and prev_names["plural"]:
                        candidates.append((idx, w, prev_names["plural"][-1]))
                    elif w in CATEGORY["first"] and prev_names["first"]:
                        candidates.append((idx, w, prev_names["first"][-1]))
                    elif w in CATEGORY["plural"] and prev_names["subject"]:
                        candidates.append((idx, w, prev_names["subject"][-1]))
                    else:
                        for k, v in CATEGORY.items():
                            if prev_names[k] and w in v:
                                candidates.append((idx, w, prev_names[k][-1]))
                        else:
                            if prev_names["subject"] and \
                                    w not in CATEGORY["first"]:
                                candidates.append(
                                    (idx, w, prev_names["subject"][-1]))
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
