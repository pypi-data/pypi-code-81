
from typing import Any, Dict, List, Optional, Text, Union, Type

from rasa.nlu.components import Component
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.config import RasaNLUModelConfig

from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
    INTENT,
    MESSAGE_ATTRIBUTES,
    ENTITIES,
)

from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer
# from pyspace.nlp.toolkit.zemberek import normalize, lemmatize

from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer

import re
import string
import copy

##########
import os

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
    INTENT,
    MESSAGE_ATTRIBUTES,
    ENTITIES,
)

##########


class PyspaceNormalizer(Component):

    def normalize_tokens(self, tokens):
        # [self.normalize_token(t) for t in tokens]
        return False
    def normalize_text(self, text):
        return False

    def normalize_message(self, message):

        if self.normalize_tokens(["message"]) != False:
            
            tokens = [t.text for t in message.data["tokens"] if t.text != '__CLS__']

            ###########################################################################
            
            tokens = self.normalize_tokens(tokens) 

            ###########################################################################

            if self.normalize_text("message") != False:
                norm = self.normalize_text(message.text.replace('__CLS__','').strip())
            else:
                norm = " ".join(tokens)
            message.text = norm
            message.set(TEXT, norm)
            
            tokens = Tokenizer._convert_words_to_tokens(tokens, norm)
            tokens = Tokenizer.add_cls_token(tokens, TEXT)
            message.set(TOKENS_NAMES[TEXT], tokens)
            
        elif self.normalize_text("message") != False:

            norm = self.normalize_text(message.text)

            message.text = norm
            message.set(TEXT, norm)


    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        for message in training_data.training_examples:
            self.normalize_message(message)

    def process(self, message: Message, **kwargs: Any):

        self.normalize_message(message)

##########################################################################################3
##########################################################################################3

class ZemberekNormalizer(PyspaceNormalizer):

    
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        from pyspace.nlp.toolkit.zemberek import normalize
        self.normalize = normalize
        super().__init__(component_config)
    
    def normalize_text(self, text):
        return self.normalize(text)


class ZemberekLemmatizer(PyspaceNormalizer):

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        from pyspace.nlp.toolkit.zemberek import lemmatize
        self.lemmatize = lemmatize
        super().__init__(component_config)
        
    def normalize_tokens(self, tokens):
        return [self.lemmatize(t) for t in tokens]

class TurkishCharacterNormalizer(PyspaceNormalizer):

    def normalize_tokens(self, tokens):
        return [xNormalizer.tr_normalize(t) for t in tokens]

    def normalize_text(self, text):
        return xNormalizer.tr_normalize(text)

class PunctuationNormalizer(PyspaceNormalizer):

    def normalize_tokens(self, tokens):
        
        output = []
        for t in tokens: 
            temp = re.sub(fr"""[{re.escape(string.punctuation)}]""", '', t).strip()
            if temp != '':
                output.append(temp)
        return output


class LowercaseNormalizer(PyspaceNormalizer):

    defaults = {
        "lang": "EN",
    }

    def normalize_tokens(self, tokens):
        return [xNormalizer.lower(t, lang=self.component_config["lang"]) for t in tokens]
    
    def normalize_text(self, text):
        return xNormalizer.lower(text, lang=self.component_config["lang"])

class StopwordsNormalizer(PyspaceNormalizer):

    defaults = {
        "lang": "TR",
    }
    

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        # TODO
        # from pyspace_resources.stopwords.turkish import stopwords
        self.stopwords = self.component_config["stopwords"]

    def normalize_tokens(self, tokens):

        return [t for t in tokens if t not in self.stopwords]
    


##########################################################################################3
##########################################################################################3
class EntityNormalization(Component):

    defaults = {
        'normalization_config' : [
            ['entities', 'DIETClassifier', 'B-AMOUNT-OF-MONEY', '', 'A'],
        ],
    }

    def __init__(self, component_config: Dict[Text, Any] = None,) -> None:
        super(EntityNormalization, self).__init__(component_config)

    def normalize(self, message, ):

        # assert message.data["tokens"] == message.get(TOKENS_NAMES[TEXT])
        tokens = message.get(TOKENS_NAMES[TEXT])

        for n in self.component_config["normalization_config"]:
            attr, classifier_name, entity_name, role, replacement = n

            entities = message.get(attr)
            # entities = [e for e in entities if e['extractor'] in [classifier_name] and e['entity'] in [entity_name] ]
            entities = [e for e in entities if e['extractor'] in [classifier_name] and e['entity'] in [entity_name] and role in [e.get("role", "")] ]
            entities = sorted(entities, key=lambda e:e['start'])

            result = []
            e_end = -1
            for token in tokens:
                # token['normalized'] = True
                if e_end >= token.end:
                    continue  
                for e in entities:
                    startbool = token.start >= e['start']
                    endbool = token.end <= e['end']

                    if startbool and endbool:
                        token.text = replacement
                        token.lemma = token.text
                        token.end = e['end']
                result.append(token)
                e_end = token.end
            tokens = result
            # for token in tokens:
            #     for e in entities:
            #         startbool = token.start >= e['start']
            #         endbool = token.end <= e['end']
            #         if startbool and endbool:
            #             token.text = replacement
            #             token.lemma = token.text

        message.set(TOKENS_NAMES[TEXT], tokens)

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        for message in training_data.training_examples:
            self.normalize(message,)            

    def process(self, message: Message, **kwargs: Any):
        self.normalize(message,)


class EntityNormalizationBackup(Component):
    def __init__(self, component_config: Dict[Text, Any] = None,) -> None:
        super(EntityNormalization, self).__init__(component_config)

    def normalize(self, message, entities=[]):
    
        tokens = message.get(TOKENS_NAMES[TEXT])

        entities = sorted(entities, key=lambda e:e['start'])

        for token in tokens:
            
            for e in entities:
                startbool = token.start >= e['start']
                endbool = token.end <= e['end']

                if startbool and endbool:
                    
                    
                    if self.print_example_count != 0:

                        if token.text not in e['value']:
                            print('Token text is not in entity value.')

                            self.print_example_count -= 1

                            print(message.text)
                            print(token.text, token.start, token.end)
                            print(e)
                            print(entities)
                            print()

                    # assert token.text in e['value']
                    token.text = e['entity'] if 'role' not in e else e['entity'] + '-' +e['role']
                    token.lemma = token.text
                    ## TODO
                    ## if e['start'] != token.start:
                    ## ## e['entity].replace('B-', 'I-')

                    # {'entity': 'B-DURATION',
                    # 'start': 0,
                    # 'end': 1,
                    # 'role': 'YEAR',
                    # 'value': '1',
                    # 'extractor': 'DIETClassifierExtended'},
                    pass

        message.set(TOKENS_NAMES[TEXT], tokens)

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        print('  train function')
        self.print_example_count = 5

        for message in training_data.training_examples:
            entities = message.get('norm_ent')
            self.normalize(message, entities)            

    def process(self, message: Message, **kwargs: Any):

        print('  process function')
        self.print_example_count = 0
        entities = message.get(ENTITIES, [])
        entities = [e for e in entities if e['extractor'] in ['DIETClassifierExtended', 'DIETClassifier']]
        self.normalize(message, entities)


class DucklingEntityNormalizationBackup(Component):
    def __init__(self, component_config: Dict[Text, Any] = None,) -> None:
        super(DucklingEntityNormalization, self).__init__(component_config)

    def normalize(self, message, entities=[]):
    
        tokens = message.get(TOKENS_NAMES[TEXT])

        entities = sorted(entities, key=lambda e:e['start'])

        for token in tokens:
            
            for e in entities:
                startbool = token.start >= e['start']
                endbool = token.end <= e['end']

                if startbool and endbool:
                    
                    
                    if self.print_example_count != 0:

                        if token.text not in e['value']:
                            print('Token text is not in entity value.')

                            self.print_example_count -= 1

                            print(message.text)
                            print(token.text, token.start, token.end)
                            print(e)
                            print(entities)
                            print()

                    # assert token.text in e['value']
                    token.text = e['entity'] if 'role' not in e else e['entity'] + '-' +e['role']
                    token.lemma = token.text
                    ## TODO
                    ## if e['start'] != token.start:
                    ## ## e['entity].replace('B-', 'I-')

                    # {'entity': 'B-DURATION',
                    # 'start': 0,
                    # 'end': 1,
                    # 'role': 'YEAR',
                    # 'value': '1',
                    # 'extractor': 'DIETClassifierExtended'},
                    pass

        message.set(TOKENS_NAMES[TEXT], tokens)

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        print('  train function')
        self.print_example_count = 5

        for message in training_data.training_examples:
            entities = message.get(ENTITIES, [])
            entities = [e for e in entities if e['extractor'] in ['DucklingHTTPExtractor', 'DucklingExtractor', 'DucklingExtractorExtended']]
            self.normalize(message, entities)            

    def process(self, message: Message, **kwargs: Any):

        print('  process function')
        self.print_example_count = 0
        entities = message.get(ENTITIES, [])
        entities = [e for e in entities if e['extractor'] in ['DucklingHTTPExtractor', 'DucklingExtractor', 'DucklingExtractorExtended']]
        self.normalize(message, entities)


###########################################################################################


class EntityMergeSplitSelectHelper:

    @staticmethod
    def base_func_to_merge_entity_subset_without_condition(entities):

        if len(entities) == 1:
            return entities
        else:
            entities_copy = copy.deepcopy(entities)

            temp_value = ""
            prev_index = entities[0]['start']
            for e in entities:
                temp_value += " "*(e['start'] - prev_index) + e['value']
                prev_index = e['end']
            
            entities[0]['value'] = temp_value
            entities[0]['end'] = entities[-1]['end']
            entities[0]['raw'] = entities_copy

            return [entities[0]]

    @staticmethod
    def base_func_to_merge_entity_subset(message, entities, ):
        temp = entities

        if len(temp) == 1:
            return temp
            
        else:
            if all([ temp[i+1]['start'] - temp[i]['end'] <= 1 for i in range(len(temp)-1)]):
                temp_value = message.text[temp[0]['start']:temp[-1]['end']]
                temp_value_norm = xNormalizer.tr_normalize(temp_value).lower()
                
                if all( [xNormalizer.tr_normalize(tt['value']).lower() in temp_value_norm for tt in temp]):
                    temp_copy = copy.deepcopy(temp)

                    temp[0]['value'] = temp_value
                    temp[0]['end'] = temp[-1]['end']
                    temp[0]['raw'] = temp_copy

                    return [temp[0]]
                else:
                    print()
                    print('Model entities are consecutive but not match with message. They are not merged.')
                    print(temp_value)
                    # print(model_entities)
                    print(temp)
                    return temp

            else:
                print()
                print('Model entities are not consecutive. They are not merged.')
                # print(model_entities)
                print(temp)
                return temp

    @staticmethod
    def split_one_entity(e):
        result = []
        
        temp_spaces = []
        for match in re.finditer(r"\s+", e['value']):
            temp_spaces.append(match.end() - match.start())
        temp_spaces += [0]

        start_index = e['start']
        for value_i, space_i in zip( re.split('\s+', e['value']), temp_spaces ):
            e_i = copy.deepcopy(e)
            e_i['start'] = start_index
            e_i['end'] = start_index + len(value_i)
            e_i['value'] = value_i
            start_index = start_index + len(value_i) + space_i

            result.append(e_i)

        return result

    @staticmethod
    def split_rasa_entity_merge(entities):
        entities_updated = entities

        other_entities = [e for e in entities_updated if "DIET" not in e['extractor'] ]
        model_entities = [e for e in entities_updated if "DIET" in e['extractor'] ]
        model_entities = sorted(model_entities, key=lambda x: x['start'])

        splitted_model_entities = []
        for e in model_entities:
            if ' ' not in e['value']:
                splitted_model_entities.append(e)

            else:
                if e['entity'][:2] == 'B-':
                    splitted_model_entities.extend(EntityMergeSplitSelectHelper.split_one_entity(e))

                elif e['entity'][:2] == 'I-':
                    splitted_model_entities.append(e)

                else:
                    splitted_model_entities.extend(EntityMergeSplitSelectHelper.split_one_entity(e))


            entities_updated = splitted_model_entities + other_entities
        
        return entities_updated

    @staticmethod
    def merge_BI_entities(message, entities):
        entities_updated = entities
        
        other_entities = [e for e in entities_updated if "DIET" not in e['extractor'] ]
        model_entities = [e for e in entities_updated if "DIET" in e['extractor'] ]
        model_entities = sorted(model_entities, key=lambda x: x['start'])

        merged_model_entities = []
        model_entities.append({'entity':'dummy', 'value':'dummy',})
        temp = []
        for e in model_entities:
            if temp == []:
                temp.append(e)
            else:
                if e['entity'].startswith('I-'):
                    temp.append(e)
                else:
                    merged_model_entities.extend(EntityMergeSplitSelectHelper.base_func_to_merge_entity_subset(message, temp))        
                    temp = []
                    temp.append(e)


        entities_updated = merged_model_entities + other_entities

        return entities_updated

    @staticmethod
    def merge_same_entities(message, entities):
        entities_updated = entities
        
        other_entities = [e for e in entities_updated if "DIET" not in e['extractor'] ]
        model_entities = [e for e in entities_updated if "DIET" in e['extractor'] ]
        model_entities = sorted(model_entities, key=lambda x: x['start'])

        tokens = [t for t in message.data["tokens"] if t.text != '__CLS__']

        for token in tokens:
            linked_entity_counter = 0
            for entity in model_entities:
                if token.start == entity['start']:
                    token.linked_entity = entity
                    linked_entity_counter += 1
            if linked_entity_counter > 1:
                print('problem')
                print(tokens)
                print(entities)
                print()
                print(token)
                print()

        merged_model_entities = []
        temp = []
        for token in tokens + [{'token':'dummy',}]:
            if temp == []:
                if hasattr(token, 'linked_entity'):
                    temp.append(token.linked_entity)
                else:
                    continue
            else:
                if hasattr(token, 'linked_entity'):

                    if temp[0]['entity'] == token.linked_entity['entity']:
                        temp.append(token.linked_entity)

                    else:
                        merged_model_entities.extend( EntityMergeSplitSelectHelper.base_func_to_merge_entity_subset_without_condition(temp) )
                        
                        temp = []
                        temp.append(token.linked_entity)
                else:
                    merged_model_entities.extend( EntityMergeSplitSelectHelper.base_func_to_merge_entity_subset_without_condition(temp) )
                        
                    temp = []

        entities_updated = merged_model_entities + other_entities

        return entities_updated

    @staticmethod
    def merge_custom_entities__money_currency(message, entities):
        entities_updated = entities

        other_entities = [e for e in entities_updated if "DIET" not in e['extractor'] ]
        model_entities = [e for e in entities_updated if "DIET" in e['extractor'] ]
        model_entities = sorted(model_entities, key=lambda x: x['start'])

        merged_model_entities = []
        model_entities.append({'entity':'dummy', 'value':'dummy',})
        temp = []
        for e in model_entities:
            if temp == []:
                temp.append(e)
            else:
                # if temp[-1]['entity'] in ['B-AMOUNT-OF-MONEY','I-AMOUNT-OF-MONEY', 'B-amount', 'I-amount'] and e['entity'] in ['B-currency']:
                if temp[-1]['entity'] in ['B-AMOUNT-OF-MONEY', 'B-amount',] and e['entity'] in ['B-currency']:
                    if 'role' in temp[-1] or 'role' in e:
                        try:
                            assert temp[-1]['role'] == e['role']
                            # merge B-AMOUNT-OF-MONEY/from and B-currency/from, and to-to pair.
                            temp.append(e)
                        except:
                            # do not merge B-AMOUNT-OF-MONEY/from and B-currency/to
                            merged_model_entities.extend(EntityMergeSplitSelectHelper.base_func_to_merge_entity_subset(message, temp))        
                            temp = []
                            temp.append(e)
                    else:
                        # merge B-AMOUNT-OF-MONEY and B-currency
                        temp.append(e)
                else:
                    merged_model_entities.extend(EntityMergeSplitSelectHelper.base_func_to_merge_entity_subset(message, temp))        
                    temp = []
                    temp.append(e)


        entities_updated = merged_model_entities + other_entities
        return entities_updated

    @staticmethod
    def merge_custom_entities__account_account__num_currency(message, entities):
        entities_updated = entities

        entities_updated = sorted(entities_updated, key=lambda x: x['start'])
        merged_entities_updated = []
        
        entities_updated.append({'entity':'dummy', 'value':'dummy',})
        
        temp = []
        for e in entities_updated:
            if temp == []:
                temp.append(e)
            else:
                if temp[-1]['entity'] in ['account'] and temp[-1]['extractor'] in ['RegexEntityExtractor'] and e['entity'] in ['account'] and e['extractor'] in ['RegexEntityExtractor']:
                    temp.append(e)
                elif temp[-1]['entity'] in ['<num>'] and temp[-1]['extractor'] in ['RasaSpacyTokenizer'] and e['entity'] in ['B-currency'] and "DIET" in e['extractor']:
                    temp.append(e)
                else:
                    merged_entities_updated.extend(EntityMergeSplitSelectHelper.base_func_to_merge_entity_subset(message, temp))        
                    temp = []
                    temp.append(e)


        entities_updated = merged_entities_updated
        return entities_updated
    
    @staticmethod
    def sort_entities_with_config(entities, config):
        ## SORT WITH PRIORITY
        ## KEEP AT LAST IF NOT IN PRIORITY

        entities_updated = entities
        priority_config = config

        temp = []
        tempothers = []
        tempdict = {}
        
        for eidx, entity in enumerate(entities_updated):
            tempdict[eidx] = False

        for priority_i in priority_config:
            for eidx, entity in enumerate(entities_updated):

                if priority_i[0] in entity['extractor'] and priority_i[1] == entity['entity']:
                    temp.append(entity)
                    tempdict[eidx] = True
                    
        for eidx, entity in enumerate(entities_updated):
            if not tempdict[eidx]:
                temp.append(entity)
                
        entities_updated = temp
        temp = []

        return entities_updated

    @staticmethod
    def select_entities_when_multiple(entities):
        ## IF THERE ARE MORE THAN ONE MATCH FOR A TOKEN, SELECT THE FIRST ONE IN PRIORITY 
        ## AFTER FIRST ONE, KEEP IN OTHERS
        entities_updated = entities

        temp = []
        tempspan = []
        tempdict = {}
        
        for entity in entities_updated:
            ## NOTE if 22,25 in tempdict, and an entity with 16,28 comes, 16,28 stays
            overlapidx = -1
            if entity['start'] in tempdict:
                overlapidx = entity['start']
            elif entity['end']-1 in tempdict:
                overlapidx = entity['end']-1

            if overlapidx == -1:
                entity['others'] = []
                temp.append(entity)
                for idx in list(range(entity['start'],entity['end'])):
                    tempdict[idx] = entity
            else:
                tempdict[overlapidx]['others'].append(entity)

        # for entity in entities_updated:
        #     if not (entity['start'] in tempspan or entity['end'] in tempspan):
        #         temp.append(entity)
        #         tempspan.append(entity['start'])
        #         tempspan.append(entity['end'])

        entities_updated = temp
        temp = []

        return entities_updated



class EntityMergeSame(Component):

    def process(self, message: Message, **kwargs: Any) -> None:
        entities = message.get("entities", [])
        entities_updated = copy.deepcopy(entities)

        ############################################################################
        
        entities_updated = EntityMergeSplitSelectHelper.merge_same_entities(message, entities_updated)
        message.set("entities", entities_updated, add_to_output=True)

