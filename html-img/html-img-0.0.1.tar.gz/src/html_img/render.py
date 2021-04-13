import os
import webbrowser
from pathlib import Path


def img_to_html(img_path = "test.png", out_file = "index.html", open_out_file = True):
  """
  Render a HTML file with an embedded image file

  All image formats that are supported by the <img> tag are valid. For reference, see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img

  img_path        : Path to image file to be embedded.
  out_file        : Path to (over)write output to.
  open_out_file   : Boolean. If True, the file is opened in you web browser.
  """

  prestring = """<html>
  <body style="margin: 0; display: flex; align-items: center; justify-content: center;">
    <img src=\""""

  poststring = """\" />
  </body>
</html>
"""
  out_file_full_path = str(Path(out_file).resolve())
  img_path_full_path = str(Path(img_path).resolve())

  with open(out_file, 'w+') as f:
    f.write(prestring)
    f.write(img_path_full_path)
    f.write(poststring)

  if open_out_file:
    webbrowser.open("file://" + out_file_full_path)
