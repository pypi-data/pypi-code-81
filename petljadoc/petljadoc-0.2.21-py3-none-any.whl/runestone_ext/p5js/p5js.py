__author__ = 'petlja'

import os
import shutil

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive


def setup(app):
    app.connect('html-page-context', html_page_context_handler)
    app.add_directive('p5js', P5jsDirective)

    app.add_stylesheet('p5js.css')

    app.add_javascript('//toolness.github.io/p5.js-widget/p5-widget.js')
    app.add_javascript('p5js.js')
 

    app.add_node(P5jsNode, html=(visit_info_note_node, depart_info_note_node))


def html_page_context_handler(app, pagename, templatename, context, doctree):
    app.builder.env.h_ctx = context

TEMPLATE_START = """
    <div class ="p5js-editor" >
    <div class = "p5js-container">
    <div class = "p5js-resize" style="width: %(width)spx">
    <script type="text/p5"  data-id="%(divid)s" data-height="%(height)s" data-preview-width="%(canvaswidth)s">
    %(code)s

"""

TEMPLATE_END = """
     </script>
     </div>
     </div>
     </div>
"""


class P5jsNode(nodes.General, nodes.Element):
    def __init__(self, content):
        super(P5jsNode, self).__init__()
        self.components = content


def visit_info_note_node(self, node):
    node.delimiter = "_start__{}_".format(node.components['divid'])
    self.body.append(node.delimiter)
    res = TEMPLATE_START % node.components
    self.body.append(res)


def depart_info_note_node(self, node):
    res = TEMPLATE_END
    self.body.append(res)
    self.body.remove(node.delimiter)


class P5jsDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    has_content = True
    option_spec = {}
    option_spec.update({
        'folder': directives.unchanged,
        'script': directives.unchanged,
        'images': directives.unchanged,
        'width': directives.unchanged,
        'height': directives.unchanged,
        'canvaswidth': directives.unchanged,
    })
    def run(self):


        env = self.state.document.settings.env
        if 'width' not  in self.options:
            self.options['width'] = '750'
        if 'height' not in self.options:
            self.options['height'] = '500'
        if 'canvaswidth' not in self.options:
            self.options['canvaswidth'] = '500'
        if 'folder' not in self.options:
            self.error('No folder path specified')      

        if 'images' in self.options:
            self.options['images'] = [image.strip() for image in self.options['images'].split(',')]
        else:
            self.options['images'] = []

        fname = self.options['folder'].replace('\\', '/')
        if not os.path.isabs(fname):
            source, _ = self.state_machine.get_source_and_line()
            fname = os.path.join(os.path.dirname(source),fname)

        if 'script' not in self.options:
            self.options['code'] = "\n".join(self.content)
        else:
            path = os.path.join(fname, self.options['script'])
            try:
                with open(path, encoding='utf-8') as f:
                    self.options['code'] = html_escape(f.read())
            except:
                self.error('Source file could not be opened')
        lecture_path =  os.path.dirname(source.replace('_intermediate','_build'))
        for image in self.options['images']:
            path = os.path.dirname(os.path.join(fname, image))
            img = os.path.basename(image)
            cwd = os.path.abspath(os.getcwd())
            try:
                build_file_path = lecture_path
                src_file_path = os.path.join(path,img)
                build_file_path_img = os.path.join(lecture_path,img)
                if not os.path.exists(build_file_path):
                    os.makedirs(build_file_path)
                shutil.copyfile(src_file_path, build_file_path_img)
            except:
                self.error('Images could not be copied')

        self.options['divid'] = self.arguments[0]

        p5js = P5jsNode(self.options)

        return [p5js]

html_escape_table = {
    "&": "&amp;",
    ">": "&gt;",
    "<": "&lt;",
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)
