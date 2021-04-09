from django import template
from psu_base.classes.Log import Log
from psu_base.templatetags.tag_processing import supporting_functions as support
from psu_base.services import utility_service
from django.utils.html import format_html
from django.template import TemplateSyntaxError
from psu_infotext.services import infotext_service

register = template.Library()
log = Log()


@register.simple_tag(takes_context=True)
def infotext(context, code, alt, replacements=None, auto_prefix=True, group_title=None):
    """
    Render user-editable text content
    """
    log.trace()
    attrs = {'code': code, 'alt': alt, 'auto_prefix': str(auto_prefix)}
    if replacements:
        attrs['replacements'] = replacements
    if group_title:
        attrs['group_title'] = group_title

    return prepare_infotext(attrs, alt)


@register.tag()
def infotext_block(parser, token):
    """
    Render user-editable text content
    """
    log.trace()
    tokens = token.split_contents()
    try:
        nodelist = parser.parse((f"end_{tokens[0]}",))
        parser.delete_first_token()
    except TemplateSyntaxError:
        nodelist = None

    return InfotextNode(nodelist, tokens)


class InfotextNode(template.Node):
    def __init__(self, nodelist, tokens):
        self.nodelist = nodelist
        self.tokens = tokens

    def render(self, context):
        log.trace()
        attrs, body = support.get_tag_params(self.nodelist, self.tokens, context)
        return prepare_infotext(attrs, body)


def prepare_infotext(attrs, alt_text):
    """
    Prepare infotext for both tags (inline and block)
    """
    code = attrs.get('code')
    if code:
        del attrs['code']
    return format_html(infotext_service.get_infotext(code, alt_text, **attrs))
