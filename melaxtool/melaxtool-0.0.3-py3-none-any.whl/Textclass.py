import json


class Text:
    def __init__(self, dic):
        self.dic = dic
        self.output = json.loads(dic['output'])
        self.bratFile = json.loads(dic['bratFile'])
        self.bratSem = json.loads(dic['bratSem'])

    def getText(self):
        return self.bratFile['text']
    def getTextLen(self):
        return len(self.bratFile['text'])
    def getEntityCount(self):
        return len(self.output['entities'].keys())
    def getRelationCount(self):
        return len(self.output['relations'])
    def getEntity(self):
        allText = self.bratFile['text']
        ret = ""
        for key, val in self.output['entities'].items():
            if 'begin' in val:
                begin = int(val['begin'])
            else:
                begin = "N/A"
            if 'end' in val:
                end = int(val['end'])
            else:
                end = 'N/A'
            if 'begin' in val and 'end' in val:
                text = allText[begin:end]
            else:
                text = "N/A"
            if "semanticTag" in val:
                semanticTag = val['semanticTag']
            else:
                semanticTag = "N/A"
            if 'cui' in val:
                cui = val['cui']
            else:
                cui = "N/A"
            if 'attrs' in val:
                if 'umlsCuiDesc' in val['attrs']:
                    umlsCuiDesc = val['attrs']['umlsCuiDesc']
                else:
                    umlsCuiDesc = 'N/A'
            else:
                umlsCuiDesc = 'N/A'

            entity = str(key) + "\t" + str(begin) + "\t" +\
                str(end) + "\t" + text + "\t" + semanticTag + "\t" + cui\
                + "\t" + umlsCuiDesc

            ret = ret + "\n" + entity
        return ret


    def getRelation(self):
        ret = ""
        relations = self.output['relations']
        if len(relations)==0:
            return "null"
        for val in relations:
            if "semanticTag" in val:
                semanticTag = val['semanticTag']
            else:
                semanticTag = 'N/A'

            if 'fromEnt' in val:
                fromEnt = val['fromEnt']
            else:
                fromEnt = 'N/A'

            if 'toEnt' in val:
                toEnt = val['toEnt']
            else:
                toEnt = 'N/A'

            relation = "sem=[" + semanticTag + "]. from=[" + fromEnt + "],\tto=[" + toEnt + "]"
            ret = ret + "\n" + relation
        return ret


