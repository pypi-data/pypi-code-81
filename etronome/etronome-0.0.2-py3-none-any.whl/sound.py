from pathlib import Path
import subprocess
from typing import Union


def play_sound(sound_file: Union[str, Path]) -> None:
    subprocess.Popen(['aplay', '-q', sound_file])
