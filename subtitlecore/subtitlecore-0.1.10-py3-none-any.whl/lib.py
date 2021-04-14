import re

def filter_typos(sentence):
  """Replace typo symbols often appeared in subtitle, such as ``\\n``, ``-``, ``[``, ``]``, ``{``, ``}``

  Args:
    sentence (str): A sentence to be corrected about the typos.

  Returns:
    str: A fixed sentence.
  """
  filtered = sentence.replace("♪","").replace("\n", " ").replace("-", "")
  filtered = re.sub(r'[\[\{].*[\}\]]:?', "", filtered).replace("  ", " ")
  return filtered.strip()


