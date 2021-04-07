#!/usr/bin/env python
# coding: utf-8

import base64
import json
import os
import requests

from melaxtool.Textclass import Text


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
            print_response(json.loads(rsp.content)['data'])
            return {'status_code': 200, 'output': json.loads(rsp.content)['data']}
            # return {'status_code': 200, 'output': json.loads(json.loads(rsp.content)['output'])}
        return {'status_code': rsp.status_code, 'content': str(rsp.content, 'utf-8')}


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


def print_response(dic):
    print("rsp.jason() dic: ", dic)
    print("dic output: ", dic['output'])
    text = Text(dic)
    print()
    print()
    print("The Text is [{}]".format(text.getText()))
    print("File length of the document is [{}]".format(text.getTextLen()))
    print("Named entity count:[{}]".format(text.getEntityCount()))
    print('Relation count:[{}]'.format(text.getRelationCount()))
    print("Named entities: {}".format(text.getEntity()))
    print("Relations: {}".format(text.getRelation()))


if __name__ == '__main__':
    input = "A developmentally appropriate group oriented therapy program was the primary treatment modality for this adolescent.  He participated in at least eight psychoeducational and activity groups.  The attending psychiatrist provided evaluation for and management of psychotropic medications and collaborated with the treatment team.  The clinical therapist facilitated individual, group, and family therapy at least twice per week. COURSE IN HOSPITAL:  During his hospitalization, the patient was seen initially as very depressed, withdrawn, some impulsive behavior observed, also oppositional behavior was displayed on the unit.  The patient also talked with a therapist about his family conflicts.  He was initiated on an antidepressant medication, Zoloft, and he continued with Adderall.  He responded well to Zoloft, was less depressed.  He continued with behavior problems and mood swings.  A mood stabilizer was added to his treatment and with a positive response to it. DIAGNOSTIC AND THERAPEUTIC TEST-EVALUATIONS:  Sleep-deprived EEG was done, which was reported as normal.  His last Depakote level was 57 as per today."
    # input = "cancer "
    client = MelaxClient('/Users/lvjian/key.txt')
    response = client.invoke(input, "default_pipeline_1")
    print(response)
