from typing import Union

from cms.models import EmptyTitle
from cms.models import Page
from cms.models import Title
from django.db.models.signals import post_save
from django.dispatch import receiver
from fieldsignals import post_save_changed


@receiver(post_save, sender=Page)
def fix_page_slugs(sender, instance: Page, **kwargs):
    _update_child_pages(instance)


@receiver(post_save_changed, sender=Title, fields=['slug', 'path'])
def fix_title_path(sender, instance: Title, **kwargs):
    _update_child_pages(instance.page)


def _update_child_pages(page: Page):
    for language in page.get_languages():
        _update_title_path(page, language)
        for child_page in page.get_child_pages():
            _update_title_path(child_page, language)


def _update_title_path(page: Page, language: str):
    page_title: Union[Title, EmptyTitle] = page.get_title_obj(language, fallback=False)
    is_title_exists = type(page_title) == Title

    if is_title_exists:
        is_title_has_url_overwrite_and_path_update_breaks_it = page_title.has_url_overwrite

        if is_title_has_url_overwrite_and_path_update_breaks_it:
            page_title.save()
        else:
            page._update_title_path(language)
