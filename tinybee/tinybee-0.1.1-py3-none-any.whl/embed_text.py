"""Embed text of list of tesxts."""
from typing import List, Union

import more_itertools as mit

# import numpy as np
from logzero import logger
from alive_progress import alive_bar

from fetch_embed import fetch_embed


# fmt: off
def embed_text(
    text: Union[str, List[str]],
    chunk_size: int = 32,
    livepbar: bool = True,  # need to turn it off in pytest
) -> List[float]:
    """Embed text or list of texts.

    Args:
        text: strings or list of string for embedding
        chunk_size: default 32
        livepbar: default True, shows progress bar
    Returns:
        embedding of 512-dimensional vectors
    """
    # fmt: on
    if isinstance(text, str):
        text = [text]
    tot, rem = divmod(len(text), chunk_size)

    res = []

    def func_():
        try:
            _ = fetch_embed(item, livepbar=False)
        except Exception as exc:
            logger.error(exc)
            raise
        res.extend(_)

    if livepbar:
        with alive_bar(tot + bool(rem)) as pbar:
            for item in mit.chunked(text, chunk_size):
                func_()
                pbar()
    else:
        for item in mit.chunked(text, chunk_size):
            func_()

    return res
