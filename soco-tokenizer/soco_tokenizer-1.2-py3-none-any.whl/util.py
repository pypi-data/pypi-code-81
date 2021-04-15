import requests
from torch import Tensor, device
import torch
from tqdm import tqdm
import sys
import importlib
import numpy as np
import re

def batch_to_device(batch, target_device: device):
    """
    send a batch to a device

    :param batch:
    :param target_device:
    :return: the batch sent to the device
    """
    features = batch['features']
    for paired_sentence_idx in range(len(features)):
        for feature_name in features[paired_sentence_idx]:
            features[paired_sentence_idx][feature_name] = features[paired_sentence_idx][feature_name].to(target_device)

    labels = batch['labels'].to(target_device)
    return features, labels


def http_get(url, path):
    file_binary = open(path, "wb")
    req = requests.get(url, stream=True)
    if req.status_code != 200:
        print("Exception when trying to download {}. Response {}".format(url, req.status_code), file=sys.stderr)
        req.raise_for_status()

    content_length = req.headers.get('Content-Length')
    total = int(content_length) if content_length is not None else None
    progress = tqdm(unit="B", total=total, unit_scale=True)
    for chunk in req.iter_content(chunk_size=1024):
        if chunk: # filter out keep-alive new chunks
            progress.update(len(chunk))
            file_binary.write(chunk)
    progress.close()


def fullname(o):
  # o.__module__ + "." + o.__class__.__qualname__ is an example in
  # this context of H.L. Mencken's "neat, plausible, and wrong."
  # Python makes no guarantees as to whether the __module__ special
  # attribute is defined, so we take a more circumspect approach.
  # Alas, the module name is explicitly excluded from __qualname__
  # in Python 3.

  module = o.__class__.__module__
  if module is None or module == str.__class__.__module__:
    return o.__class__.__name__  # Avoid reporting __builtin__
  else:
    return module + '.' + o.__class__.__name__


def import_from_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "%s doesn't look like a module path" % dotted_path
        raise ImportError(msg)

    module = importlib.import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (module_path, class_name)
        raise ImportError(msg)


class Pack(dict):
    def __getattr__(self, name):
        return self[name]

    def clone_dict(self, x):
        for k, v in list(x.items()):
            self[k] = v

    def add(self, **kwargs):
        for k, v in list(kwargs.items()):
            self[k] = v

    def copy(self):
        pack = Pack()
        for k, v in list(self.items()):
            if type(v) is list:
                pack[k] = list(v)
            else:
                pack[k] = v
        return pack


class ZhNumberConverter(object):
    common_used_numerals_tmp = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                                '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000}
    common_used_numerals = {}
    for key in common_used_numerals_tmp:
        common_used_numerals[key] = common_used_numerals_tmp[key]

    def chinese2digits(self, uchars_chinese):
        total = 0
        r = 1  # 表示单位：个十百千...
        for i in range(len(uchars_chinese) - 1, -1, -1):
            val = self.common_used_numerals.get(uchars_chinese[i])
            if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
                if val > r:
                    r = val
                    total = total + val
                else:
                    r = r * val
                    # total =total + r * x
            elif val >= 10:
                if val > r:
                    r = val
                else:
                    r = r * val
            else:
                total = total + r * val
        return total

    num_str_start_symbol = ['一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十']
    more_num_str_symbol = ['零', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿']

    def changeChineseNumToArab(self, oriStr):
        lenStr = len(oriStr)
        aProStr = ''
        if lenStr == 0:
            return aProStr

        hasNumStart = False
        numberStr = ''
        for idx in range(lenStr):
            if oriStr[idx] in self.num_str_start_symbol:
                if not hasNumStart:
                    hasNumStart = True

                numberStr += oriStr[idx]
            else:
                if hasNumStart:
                    if oriStr[idx] in self.more_num_str_symbol:
                        numberStr += oriStr[idx]
                        continue
                    else:
                        numResult = str(self.chinese2digits(numberStr))
                        numberStr = ''
                        hasNumStart = False
                        aProStr += numResult

                aProStr += oriStr[idx]
                pass

        if len(numberStr) > 0:
            resultNum = self.chinese2digits(numberStr)
            aProStr += str(resultNum)

        return aProStr


def set_seed(seed):
    """Sets random seed everywhere."""
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
    np.random.seed(seed)


def norm_sent(text):
    if text is None:
        return ''

    text = re.sub('\s+', ' ', text).strip()
    text = text.replace('\n', '').lower()
    text = re.sub('<[^<]+?>', '', text)
    return text
