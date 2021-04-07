#!/usr/bin/env python
# coding: utf-8

import base64
import json
import os

import requests


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict_to_object(dictObj):
    if not isinstance(dictObj, dict):
        return dictObj
    inst = Dict()
    for k, v in dictObj.items():
        inst[k] = dict_to_object(v)
    return inst


class NlpResult:

    def getRawText(self):
        return self.data['content']

    def getRawTextLen(self):
        return len(self.bratFile['content'])

    def getItemByType(self, type: str):
        return {key: value for key, value in self.data['indexes'].items() if type in value}

    def getAllSentence(self):
        return self.sentence[:]

    def getAllEntity(self):
        return self.entities[:]

    def getAllRelation(self):
        return self.relations[:]

    def __init__(self, code, msg, dic=None):
        self.data = dic
        self.code = code
        self.msg = msg
        self.sentence = []
        self.entities = []
        self.relations = []
        self.parse()

    def parse(self):
        for item in self.getItemByType('Sentence').items():
            if item[1] and 'Sentence' in item[1]:
                self.sentence.extend([value for value in item[1]['Sentence'].values()])

        idxdict = {'': []}

        # sen = self.sentence[idx]
        idx = 0
        self.sentence[idx]['entities'] = []
        # sen['entities'] = []
        for item in self.getItemByType('Entity').items():
            if item[1] and 'Entity' in item[1]:
                tmplist = [value for value in item[1]['Entity'].values()]

                for en in tmplist:
                    while not (
                            self.sentence[idx]['begin'] <= en['begin'] and self.sentence[idx]['end'] >= en['end']):
                        idx += 1
                        self.sentence[idx]['entities'] = []

                    self.sentence[idx]['entities'].append(en)
                    self.entities.append(en)
                    idxdict[self.key(en)] = [len(
                        self.entities) - 1, idx]

        idx = 0
        ent = self.entities[idx]
        ent['relations'] = []
        for item in self.getItemByType('Relation').items():
            if item[1] and 'Relation' in item[1]:
                tmplist = [value for value in item[1]['Relation'].values()]
                self.relations.extend(tmplist)
                for rel in tmplist:
                    key = self.key(rel['fromEnt'])
                    if 'relations' in self.entities[idxdict[key][0]]:
                        self.entities[idxdict[key][0]]['relations'].append(rel)
                    else:
                        self.entities[idxdict[key][0]]['relations'] = [rel]
                    # if key in idxdict and 'entities' in self.sentence[idxdict[key][1]]:
                    #     for en in self.sentence[idxdict[key][1]]['entities']:
                    #         if en['begin'] == rel['fromEnt']['begin'] and en['end'] == rel['fromEnt']['end']:
                    #             if 'relations' in en:
                    #                 en['relations'].append(rel)
                    #             else:
                    #                 en['relations'] = [rel]

    def key(self, en: dict):
        return str(en['begin']) + '_' + str(en['end']) + '_' + str(en['semantic'])


class MelaxClient:

    def __init__(self, key_path: str = None):
        self.key_path = key_path
        if key_path is not None:
            # read file key
            key = read_key_file(key_path)
            if key is not None:
                key_obj = verify_key(key)
                self.key = key
                self.url = key_obj['url']
                return
        key = os.environ.get("MELAX_TECH_KEY")
        if key is not None:
            key_obj = verify_key(key)
            self.key = key
            self.url = key_obj['url']

    # def invoke(self, text: str):
    #     payload = "{\"input\":\"" + str(base64.b64encode(text.encode("utf-8")), "utf-8") + "\"}"
    #     rsp = requests.request('POST', self.url, data=payload, headers=headers(self.key))
    #     if rsp.status_code == 200:
    #         return {'status_code': 200, 'output': json.loads(json.loads(rsp.content)['output'])}
    #     return {'status_code': rsp.status_code, 'content': str(rsp.content, 'utf-8')}

    def invoke(self, text: str, pipeline: str):
        # payload = "{\"input\":\"" + str(base64.b64encode(text.encode("utf-8")), "utf-8") + "\"}"
        payload = {
            "text": text,
            "pipeline": pipeline
        }
        rsp = requests.request('POST', self.url + "/api/nlp", data=json.dumps(payload), headers=headers(self.key))
        if rsp.status_code == 200:
            nlprsp = json.loads(rsp.content)
            if nlprsp and 'code' in nlprsp and nlprsp['code'] == 200:
                # print_response(nlprsp['data'])
                return NlpResult(200, '', json.loads(nlprsp['data']['output']))
            else:
                return NlpResult(nlprsp['code'], nlprsp['message'])

        return NlpResult(rsp.status_code, rsp.content)


def read_key_file(key_path: str):
    with open(key_path, mode='r') as file_obj:
        content = file_obj.read().splitlines()[0]
        return content
    return None


def verify_key(key: str):
    key_tmp = key.split('.')[1]
    if len(key_tmp) % 4 != 0:
        key_tmp += (len(key_tmp) % 4) * '='
    return json.loads(base64.b64decode(key_tmp))


def headers(key):
    return {'Content-Type': 'application/json', 'x-api-key': "Bearer " + key}


if __name__ == '__main__':
    # input = "A developmentally appropriate group oriented therapy program was the primary treatment modality for this adolescent.  He participated in at least eight psychoeducational and activity groups.  The attending psychiatrist provided evaluation for and management of psychotropic medications and collaborated with the treatment team.  The clinical therapist facilitated individual, group, and family therapy at least twice per week. COURSE IN HOSPITAL:  During his hospitalization, the patient was seen initially as very depressed, withdrawn, some impulsive behavior observed, also oppositional behavior was displayed on the unit.  The patient also talked with a therapist about his family conflicts.  He was initiated on an antidepressant medication, Zoloft, and he continued with Adderall.  He responded well to Zoloft, was less depressed.  He continued with behavior problems and mood swings.  A mood stabilizer was added to his treatment and with a positive response to it. DIAGNOSTIC AND THERAPEUTIC TEST-EVALUATIONS:  Sleep-deprived EEG was done, which was reported as normal.  His last Depakote level was 57 as per today."
    input = """
     Sample Type / Medical Specialty:  Discharge Summary
Sample Name: Psychiatric Discharge Summary - 1
Description:  Discharge summary of a patient with mood swings and oppositional and defiant behavior.
(Medical Transcription Sample Report)
DISCHARGE SUMMARY
SUMMARY OF TREATMENT PLANNING:
Two major problems were identified at the admission of this adolescent:
1.   Mood swings.
2.   Oppositional and defiant behavior.
A developmentally appropriate group oriented therapy program was the primary treatment modality for this adolescent.  He participated in at least eight psychoeducational and activity groups.  The attending psychiatrist provided evaluation for and management of psychotropic medications and collaborated with the treatment team.  The clinical therapist facilitated individual, group, and family therapy at least twice per week.
COURSE IN HOSPITAL:  During his hospitalization, the patient was seen initially as very depressed, withdrawn, some impulsive behavior observed, also oppositional behavior was displayed on the unit.  The patient also talked with a therapist about his family conflicts.  He was initiated on an antidepressant medication, Zoloft, and he continued with Adderall.  He responded well to Zoloft, was less depressed.  He continued with behavior problems and mood swings.  A mood stabilizer was added to his treatment and with a positive response to it.
DIAGNOSTIC AND THERAPEUTIC TEST/EVALUATIONS:  Sleep-deprived EEG was done, which was reported as normal.  His last Depakote level was 57 as per 06/04/04.
His laboratory basic metabolic panel, CBC, TSH were reported within normal limits.
CONSULTATIONS:  He was seen by our medical consultant for a complete history and medical examination.  No major acute problems were reported, only the acne.  Treatment was initiated with face wash medication.
FINAL DIAGNOSIS:
AXIS    I:        ADHD (Attention Deficit Hyperactivity Disorder), rule out Bipolar Disorder and ODD (Oppositional Defiant Disorder).
AXIS   II:  Deferred.
AXIS  III:        Acne.
AXIS  IV:        Psychosocial stressors: Severe, family conflicts and educational problems.
AXIS   V:         GAF: 45 to 50.
CONDITIONS ON DISCHARGE:  The patient had appropriate mood and was not engaging in self-injurious behavior.  He denied suicidal or homicidal ideation.
Height: 5 foot 8 inches.  Weight: 134.  Blood pressure: 120/54.  Pulse: 104.  Respirations: 18.  Temperature: 99.
PROGNOSIS:   Guarded.
DISCHARGE PLAN:    As recommended by the treatment team, the patient was discharged to an RTC (Residential Treatment Center) Program to North Star RTC.  He was transferred by personal staff of that institution.
DISCHARGE INSTRUCTIONS/MEDICATIONS:  The patient is to continue treatment at North Star RTC.  Discharge medications are Adderall XR 30 mg p.o. q. a.m., Depakote 250 mg p.o. t.i.d., Zoloft 55 mg p.o. q. a.m.  The prescription was given to the patient's representative.  As other instructions, the patient may continue treatment at North Star RTC with at least once a week family session.  The patient's representative and the patient both acknowledged that they understand all the medications prescribed and how to administer them, and the importance of the next level of care and continuing treatment.  If he experiences any side effects or has any concerns regarding his behavior, safety, immediately contact North Star Hospital.

     """
client = MelaxClient('/Users/lvjian/key.txt')
response = client.invoke(input, "document_new:$LATEST")
print(len(response.getAllSentence()))


