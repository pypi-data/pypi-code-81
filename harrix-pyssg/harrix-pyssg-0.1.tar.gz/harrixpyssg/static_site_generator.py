from .dir_md_to_dir_html import Dir_md_to_dir_html

import harrixpylib as h

class StaticSiteGenerator:
    def __init__(self, markdown_paths, output_path):
        self.markdown_paths = markdown_paths
        self.output_path = output_path

    def start(self):
        h.clear_directory(self.output_path)
        for path in self.markdown_paths:
            Dir_md_to_dir_html(path, self.output_path).start()