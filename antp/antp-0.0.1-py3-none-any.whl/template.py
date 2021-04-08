from jinja2 import Template as JinjaTemplate


class Template(object):

  def __init__(self, filename=None, text=None):
    self._filename = filename
    if filename is not None:
      self.text = self.load_text(filename)
    else:
      self.text = text

    if self.text is None:
      raise InvalidTemplateException(self.text)

    self._template = JinjaTemplate(self.text)


  @property
  def template(self):
    return self._template


  @staticmethod
  def load_text(filename):
    result = None
    if filename == '-':
      import sys
      f = sys.stdin
    else:
      f = open(filename, 'r', encoding='utf8')
    with f as file:
      result = file.read()
    return result


class InvalidTemplateException(Exception):
  pass