from typing import Iterable

from d8s_networking import get


def mp4_download(url: str) -> Iterable[bytes]:
    """."""
    result = get(url)

    for chunk in result.iter_content(chunk_size=255):
        if chunk:
            yield chunk


def mp3_download(url: str) -> Iterable[bytes]:
    yield from mp4_download(url)
