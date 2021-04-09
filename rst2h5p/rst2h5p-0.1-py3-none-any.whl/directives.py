from docutils.parsers.rst import Directive
from docutils.parsers.rst import states, directives
from docutils.nodes import General, Element

class multichoice(General, Element): pass
class singlechoice(General, Element): pass

class BaseDirective(Directive):
    final_argument_whitespace = True
    option_spec = {}
    has_content = True

    def run(self):
        self.assert_has_content()
        node = self.node_class("", **self.options)
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset,
                                node)
        return [node]

class SingleChoice(BaseDirective):
    node_class = singlechoice

class MultiChoice(BaseDirective):
    node_class = multichoice
    option_spec = {'correct': directives.positive_int_list}
