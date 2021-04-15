import setuptools
import subprocess
import platform
from pathlib import Path
from distutils.core import setup, Extension


def main():
    ext = Extension(
        'hsbg_sim',
        sources=[
            'src/enum_data.cpp', 'src/minion_events.cpp',
            'src/hero_powers.cpp', 'src/battle.cpp',
            'src/random.cpp', 'src/hsbgsimmodule.cpp'
        ],
        include_dirs=['./src'],
        extra_compile_args=['-std=c++11'] if platform.system() != 'Windows' else []
    )

    setup(name="hsbg_sim",
          version="1.0.0",
          description="Python interface for the Hearthstone Battlegrounds combat simulator.",
          author="Shon Verch",
          ext_modules=[ext],
          setup_requires=['wheel']
    )

if __name__ == "__main__":
    subprocess.run(['python', 'scripts/generate_enum_data.py', 'hsdata/CardDefs.xml'])
    main()
