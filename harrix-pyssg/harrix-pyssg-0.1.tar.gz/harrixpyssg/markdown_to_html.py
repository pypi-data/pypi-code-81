from pathlib import Path
import shutil
import markdown

import harrixpylib as h


class MarkdownToHtml:
    def __init__(self, markdown_filename, output_path):
        self.markdown_filename = Path(markdown_filename)
        self.output_path = Path(output_path)

    def start(self):
        h.clear_directory(self.output_path)

        markdown_text = h.open_file(self.markdown_filename)

        md = markdown.Markdown(extensions=['meta'])
        html = md.convert(markdown_text)

        self.copy_dirs()

        h.save_file(html, self.output_path / 'index.html')

    def copy_dirs(self):
        dirs_of_files = ['img', 'files', 'demo', 'gallery']
        for d in dirs_of_files:
            self.copy_dir(d)

    def copy_dir(self, directory):
        path_img = self.markdown_filename.parent / directory
        if path_img.is_dir():
            shutil.copytree(path_img, self.output_path /
                            directory, dirs_exist_ok=True)
