# encoding: utf-8

import os
import copy
import numpy as np
import pandas as pd

from typing import List, Union, Tuple, Optional
from collections import OrderedDict
from collections.abc import Iterable


# Define type aliases
Char = str
CharsInput = List[Char]
CharsOutput = CharsInput

Token = Char
TokenId = int
TokenInput = List[Token]
TokenOutput = TokenInput

Text = str
TextInput = List[Text]

# Slow tokenizers used to be saved in three separated files
TOKENIZER_CONFIG_FILE = "tokenizer_config.json"


class TokenizerBase:
    
    def __init__(self, **kwargs):
        # inputs and kwargs for saving and re-loading (see ``from_pretrained`` and ``save_pretrained``)
        self.init_inputs = ()
        self.init_kwargs = copy.deepcopy(kwargs)

    def tokenize(self, texts: Union[Text, TextInput, List[CharsInput]], **kwargs) -> List[str]:
        if isinstance(texts, str):
            return self._tokenize(texts)
        elif isinstance(texts, (list, tuple, np.ndarray, pd.Series)):
            return [self._tokenize(_) for _ in texts]
        else:       
            raise ValueError(
                f"type of texts unknown: {type(texts)}. "
                f"Should be one of a str, list, tuple, np.ndarray or pd.Series."
            )

    def _tokenize(self, texts: Union[Text, CharsInput], **kwargs) -> CharsOutput:
        raise NotImplementedError

    def save_pretrained(
        self, 
        save_directory: Union[str, os.PathLike],
        filename_prefix: Optional[str] = None
    ) -> Tuple[str]:

        if os.path.isfile(save_directory):
            logger.error("Provided path ({}) should be a directory, not a file".format(save_directory))
            return
        os.makedirs(save_directory, exist_ok=True)

        tokenizer_config_file = os.path.join(
            save_directory, (filename_prefix + "-" if filename_prefix else "") + TOKENIZER_CONFIG_FILE
        )

        tokenizer_config = copy.deepcopy(self.init_kwargs)
        if len(self.init_inputs) > 0:
            tokenizer_config["init_inputs"] = copy.deepcopy(self.init_inputs)
        for file_id in self.vocab_files_names.keys():
            tokenizer_config.pop(file_id, None)

        with open(tokenizer_config_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(tokenizer_config, ensure_ascii=False))
        # logger.info(f"tokenizer config file saved in {tokenizer_config_file}")
        # TODO:
        pass

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path: Union[str, os.PathLike], *init_inputs, **kwargs):
        # Prepare tokenizer initialization kwargs
        # TODO:
        filename_prefix = None
        tokenizer_config_file = os.path.join(
            save_directory, (filename_prefix + "-" if filename_prefix else "") + TOKENIZER_CONFIG_FILE
        )
        with open(tokenizer_config_file, encoding="utf-8") as tokenizer_config_handle:
            init_kwargs = json.load(tokenizer_config_handle)
        saved_init_inputs = init_kwargs.pop("init_inputs", ())
        if not init_inputs:
            init_inputs = saved_init_inputs

        # Update with newly provided kwargs
        init_kwargs.update(kwargs)

        # Instantiate tokenizer.
        try:
            tokenizer = cls(*init_inputs, **init_kwargs)
        except OSError:
            raise OSError(
                "Unable to load vocabulary from file. "
                "Please check that the provided vocabulary is accessible and not corrupted."
            )

        return tokenizer
