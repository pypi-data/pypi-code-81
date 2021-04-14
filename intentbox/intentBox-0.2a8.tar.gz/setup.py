from setuptools import setup

setup(
    name='intentBox',
    version='0.2a8',
    packages=['intentBox',
              'intentBox.coreference',
              'intentBox.intent_assistant',
              'intentBox.lang',
              'intentBox.parsers',
              'intentBox.segmentation',
              'intentBox.utils'
              ],
    url='https://github.com/HelloChatterbox/intentBox',
    license='',
    author='jarbasai',
    install_requires=["adapt-parser>=0.3.3", "padaos>=0.1.9", "auto_regex"],
    author_email='jarbasai@mailfence.com',
    extras_require={
        "extras": ["requests", "padatious>=0.4.6", "fann2>=1.0.7",
                   "pronomial>=0.0.6", "RAKEkeywords"]
    },
    description='chatterbox intent parser, extract multiple intents from a single utterance '
)
