from pathlib import Path
from .markdown_to_html import MarkdownToHtml

import harrixpylib as h

class Dir_md_to_dir_html:
    def __init__(self, markdown_path, output_path):
        self.markdown_path = Path(markdown_path).resolve()
        self.output_path = Path(output_path).resolve()
        print(self.output_path)

    def start(self):
        for item in self.markdown_path.rglob("*.md"):
            parts = list(item.parts[len(self.markdown_path.parts)::])
            if len(item.suffixes) == 1:
                parts[-1] = 'ru'
            else:
                parts[-1] = item.suffixes[-2][1:]
            MarkdownToHtml(item, self.output_path.joinpath(*parts)).start()
