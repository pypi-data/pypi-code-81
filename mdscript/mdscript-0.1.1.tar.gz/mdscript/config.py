from typing import Dict
from base_transformer import BaseTransformer


class MDScriptConfig:
    def __init__(self, transformers: Dict[str, type(BaseTransformer)]):
        self.transformers = transformers
