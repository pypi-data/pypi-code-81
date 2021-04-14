from intentBox.container import IntentBox
from os.path import join
from os import listdir, walk


class CollisionDetector:
    def __init__(self, skills_folder, blacklisted_skills=None):
        self.skills_path = skills_folder
        self.blacklisted_skills = blacklisted_skills or []
        self.box = IntentBox()
        self._skills_map = {}
        self.load_skills()

    def load_skills(self):
        for skill_folder in listdir(self.skills_path):
            for base, folders, files in walk(join(self.skills_path, skill_folder)):
                for f in files:
                    if f.endswith(".voc"):
                        name = skill_folder + ":" + f.split(".")[0]
                        self._skills_map[name] = skill_folder
                        # TODO this is very limiting but works for the standard listen block
                        self.box.register_adapt_intent_from_file(name, join(base, f))
                    elif f.endswith(".rx"):
                        self._skills_map[f] = skill_folder
                        self.box.register_adapt_regex_from_file(join(base, f))
                    elif f.endswith(".intent"):
                        name = skill_folder + ":" + f.split(".")[0]
                        self._skills_map[name] = skill_folder
                        self.box.register_padatious_intent_from_file(name, join(base, f))
                    elif f.endswith(".entity"):
                        self.box.register_padatious_entity_from_file(f, join(base, f))

    def triggered_skills(self, utterance, min_conf=0.5):
        utterance = utterance.strip() # spaces should not mess with exact matches
        intents = self.box.intent_scores(utterance)
        for idx, intent in enumerate(intents):
            intents[idx].pop("utterance")
            intents[idx]["skill"] = self._skills_map.get(intents[idx]["intent_type"])
            intents[idx]["intent_name"] = intents[idx].pop("intent_type").split(":")[-1]
            if intent["conf"] < min_conf:
                intents[idx] = None
        return [i for i in intents if i]


