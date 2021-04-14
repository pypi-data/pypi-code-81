# -*- coding: utf-8 -*-
"""``subtitlecore`` Package

This module demostrates the usage of package `subtitlecore`.

.. topic:: Install package
  
  .. code:: shell
    
    $ pip3 install --verbose subtitlecore

.. topic:: Use as executable

  .. code:: shell

    $ subtitlecore_parse2text --srtfile movie.srt --lang en

  .. code:: shell

    $ subtitlecore_parse2sens --srtfile movie.srt --lang en


.. topic:: Get time based content from subtitle file

  .. code:: python

    from subtitlecore import Subtitle

    def get_subtitle_content(srtfile, lang):
      st = Subtitle(srtfile, lang)
      for line_info in st.content:
        print(line_info)

.. topic:: Get plain text from subtitle file

  .. code:: python

    from subtitlecore import Subtitle
    
    def parse2text(srtfile, lang):
      st = Subtitle(srtfile, lang)
      text = st.plaintext()
      print(text) 

.. topic:: Parse each line in subtitle file into sentences with timestamp

  .. code:: python

    from subtitlecore import Subtitle

    def parse2sens(srtfile, lang):
      st = Subtitle(srtfile, lang)
      time_based_sens = st.sentencize()
      for l in time_based_sens:
        print(l)

"""
__version__ = '0.1.10'


from .sentencizer import Sentencizer
from .subtitle import Subtitle
