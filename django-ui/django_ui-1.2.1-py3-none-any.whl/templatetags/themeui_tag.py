from django import template
from django_ui.models import ThemeUI

register = template.Library()


@register.simple_tag()
def theme_ui():
    return ThemeUI.objects.filter(applied=True).first()


@register.simple_tag()
def is_image(value):
    img = value.name.split('/')
    return img[0] == 'original_images'
