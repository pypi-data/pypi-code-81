from django import template

from djoptimizely.services import get_feature_enabled


register = template.Library()
  
@register.simple_tag(takes_context=True)
def show_feature(context, flag_key):
    request = context['request']
    return get_feature_enabled(request, flag_key)
