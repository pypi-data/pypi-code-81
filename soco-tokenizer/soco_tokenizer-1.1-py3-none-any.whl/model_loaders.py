from soco_tokenizer.tokenizer import Tokenizer


class EncoderLoader(object):
    @staticmethod
    def load_tokenizer(model_id, access_key='', secret='', engine='oss'):
        return Tokenizer(model_id, access_key, secret, engine)

