import requests
from intentBox.coreference.base import CoreferenceSolver


class NeuralCoreferenceDemoSolver(CoreferenceSolver):

    @classmethod
    def solve_corefs(cls, text, lang="en"):
        try:
            params = {"text": text}
            r = requests.get("https://coref.huggingface.co/coref",
                             params=params).json()
            return r["corefResText"] or text
        except Exception as e:
            return text


class CogCompDemoSolver(CoreferenceSolver):
    @staticmethod
    def _cogcomp_demo(text):
        url = "https://cogcomp.org/demo_files/Coref.php"
        data = {"lang": "en", "text": text}
        r = requests.post(url, json=data)
        return r.json()

    @classmethod
    def solve_corefs(cls, text, lang="en"):
        if lang.startswith("en"):
            from intentBox.lang.en import COREFERENCE_INDICATORS_EN
            indicators = COREFERENCE_INDICATORS_EN
        elif lang.startswith("pt"):
            from intentBox.lang.pt import COREFERENCE_INDICATORS_PT
            indicators = COREFERENCE_INDICATORS_PT
        else:
            indicators = []

        try:
            data = cls._cogcomp_demo(text)
            links = data["links"]
            node_ids = {}
            replace_map = {}
            for n in data["nodes"]:
                node_ids[int(n["id"])] = n["name"]
            for l in links:
                if node_ids[l["target"]].lower() not in indicators:
                    continue
                replace_map[node_ids[l["target"]]] = node_ids[l["source"]]
            for r in replace_map:
                text = text.replace(r, replace_map[r])
            return text
        except Exception as e:
            return text
