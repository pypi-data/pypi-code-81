import json
from sklearn_model.export import Model

class JMLM(object):
    def __init__(self, model):
        self.jmlm = model

    @classmethod
    def fromFile(cls, filepath):
        model = None
        with open(filepath, "r") as jmlmfile:  
            model = json.load(jmlmfile) 
        return cls(model)

    @classmethod
    def fromString(cls, jmlm_string):
        model = json.loads(jmlm_string)
        return cls(model)

    @classmethod
    def fromModel(cls, model):
        if isinstance(model, Model):
            model = model.export()
        else:
            raise TypeError("model should be of type Model (sklearn_model.export.Model).")
        return cls(model)
        

    def extractRules(self):
        if self.jmlm["model"]["type"] != "DecisionTreeClassifier":
            raise TypeError("Extract Rules only supports model of type 'DecisionTreeClassifier'.")
        else:
            l = []
            self.traverseNode(self.jmlm["model"]["scoring_params"]["tree"], "", l)
            return l 

    @staticmethod
    def traverseNode(node, rule_so_far, l):
        suffix = ""
        if node["isleaf"]:
            l.append({"class" : node["class"], "rule": rule_so_far})
            return
        if len(rule_so_far) > 0:
            suffix = " and "
        left_rule = rule_so_far + suffix + "({0} <= {1})".format(node["field"], node["split_value"])
        right_rule = rule_so_far + suffix + "({0} > {1})".format(node["field"], node["split_value"])
        return JMLM.traverseNode(node["l"], left_rule, l), JMLM.traverseNode(node["r"], right_rule, l)
