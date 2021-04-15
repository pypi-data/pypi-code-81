from soco_tokenizer.bert_tokenizer import SocoBertTokenizer
from soco_tokenizer.cloud_bucket import CloudBucket

import os
import json


class Tokenizer(object):
    local_dir = "resources"

    def __init__(self, model_id, access_key, secret, engine):
        # check if model path is on disk. o/w download it

        if os.path.exists(os.path.join(self.local_dir, model_id, 'vocab.txt')):
            base_path = os.path.join(self.local_dir, model_id, 'vocab.txt'.format(model_id))
        else:
            bucket = CloudBucket(access_key, secret, engine)
            bucket.download_tokenizer('tokenizers', model_id, local_dir=self.local_dir)
            base_path = os.path.join(self.local_dir, model_id, '{}.txt'.format(model_id))

        final_path = os.path.join(self.local_dir, model_id, '{}.json'.format(model_id))
        config_path = os.path.join(self.local_dir, model_id, 'config.json')
        config = json.load(open(config_path, 'r'))

        # create a tokenizer
        self._tokenizer = SocoBertTokenizer(base_path, final_path, config['lang'])

    def tokenize(self, *args, **kwargs):
        return self._tokenizer.tokenize(*args, **kwargs)

    def convert_tokens_to_ids(self, *args):
        return self._tokenizer.convert_tokens_to_ids(*args)

    def convert_ids_to_tokens(self, *args):
        return self._tokenizer.convert_ids_to_tokens(*args)


if __name__ == "__main__":
    t = Tokenizer('bert-base-chinese', 'cn')
    sent = '我爱自然语言处理。什么！谁敢挑战我？'
    print(t.tokenize(sent, mode='char'))
    print(t.tokenize(sent, mode='word'))
    print(t.tokenize(sent, mode='all'))
    print(t.convert_tokens_to_ids(t.tokenize(sent, mode='all')))
    print(t.convert_ids_to_tokens(t.convert_tokens_to_ids(t.tokenize(sent, mode='all'))))
