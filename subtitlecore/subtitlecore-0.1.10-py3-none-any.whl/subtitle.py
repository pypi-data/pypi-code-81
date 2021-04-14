# -*- coding: utf-8 -*-

import webvtt
from os import path
from subtitlecore import Sentencizer
from subtitlecore.lib import filter_typos

class Subtitle:
  """Manipulate subtitle content

  Args:
    srtfile (str): subtitle file name
    lang (str, optional): subtitle language. Defaults to ``en``

  Attributes:
    file (str): subtitle file full path
    fname (str): subtitle file name
    fext (str): subtitle file extension, e.g, ``srt``, ``vtt``
    lang (str): subtitle language, e.g, ``en``, ``es``
    content (list): subtitle content stored as time-based sentences in a list 
  """

  def __init__(self, srtfile, lang="en"):
    srtfile = path.expanduser(srtfile)
    if path.exists(srtfile) and path.isfile(srtfile):
      self.file = srtfile
      self.fname, self.fext = path.splitext(path.basename(srtfile))
      self.lang = lang
      self._init_content()
    else:
      print("File {} does NOT exist !!!".format(srtfile))
      self.file, self.fname, self.lang, self.content = "", "", lang, []

 
  def _init_content(self):
    self.content = []
    obj = webvtt.from_srt(self.file)

    for index, caption in enumerate(obj.captions):
      self.content.append({
        "start": caption.start,
        "end": caption.end,
        "text": filter_typos(caption.text),
        "identifier": str(index+1)
      })

  def plaintext(self):
    """Get plain text from substitle, without time stamp involved

    Returns:
      str: Plain text of subtitle file without time stamp information
    """

    return " ".join([info["text"] for info in self.content])

  def sentenize(self):
    """Sentenize each subtitle line within time stamp 

    Returns:
      list: A list of dict object, which has keys: ``start``, ``end``, ``text``, ``identifier``, ``sens``
    """

    nlp_content = self.content.copy()
    tool = Sentencizer(self.lang)
    for line_info in nlp_content:
      line = line_info["text"]
      line_info["sens"] = tool.mark(line) 
    return nlp_content 
