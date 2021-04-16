from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'gnani_voicebiometric'
LONG_DESCRIPTION = 'This is a voicebiometric api to authenticate your voice with gnani VoiceBiometric service'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="gnani_voicebiometric",
        version=VERSION,
        author="gnani.ai",
        author_email="<api.service@gnani.ai>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        package_data={'gnani_voicebiometric_api.audio': ['*.wav'], 'gnani_voicebiometric_api': ['*.pem', '*.md','*.log']},
        include_package_data=True,
        install_requires=['requests','pytz'],
        keywords=['python', 'Voicebiometric service'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
