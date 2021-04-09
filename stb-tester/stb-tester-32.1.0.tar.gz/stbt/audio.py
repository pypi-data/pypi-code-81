# coding: utf-8

"""Stb-tester APIs for audio capture, analysis, and verification.

Copyright © 2018-2020 Stb-tester.com Ltd.

This `stbt.audio` sub-package is provided for backward compatibility; since v32
all of these names are available directly in the `stbt` namespace, for example
`stbt.get_rms_volume`.
"""

__all__ = ["AudioChunk",
           "audio_chunks",
           "get_rms_volume",
           "play_audio_file",
           "VolumeChangeDirection",
           "VolumeChangeTimeout",
           "wait_for_volume_change"]

from stbt import (
    AudioChunk,
    audio_chunks,
    get_rms_volume,
    play_audio_file,
    VolumeChangeDirection,
    VolumeChangeTimeout,
    wait_for_volume_change)
