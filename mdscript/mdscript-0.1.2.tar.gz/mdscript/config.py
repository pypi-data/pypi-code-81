from mdscript.base_transformer import BaseTransformer
from typing import Dict


class MDScriptConfig:
    def __init__(self, transformers: Dict[str, type(BaseTransformer)]):
        self.transformers = transformers
