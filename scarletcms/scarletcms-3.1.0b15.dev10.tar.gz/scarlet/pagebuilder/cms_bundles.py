from scarlet.cms import bundles, views, options
from scarlet.cms.sites import site
from scarlet.cms.forms import search_form

from . import settings, get_page_model, get_carousel_model
from .forms import (
    PAGE_EDIT_FORMSETS,
    PAGE_EDIT_FIELDSET,
    MODULE_COMBINED_FORMSET,
    EmptyPageForm,
    PageForm,
    CarouselItemInlineFormset,
)


class CarouselBundle(bundles.Bundle):
    dashboard = (("main", "Carousels"),)

    main = views.ListView()
    edit = views.FormView(formsets={"Items": CarouselItemInlineFormset()})
    add = edit

    class Meta:
        model = get_carousel_model()
        primary_model_bundle = True


class ContentModuleBundle(bundles.ObjectOnlyBundle):
    navigation = bundles.PARENT

    main = views.FormView(
        form_class=EmptyPageForm,
        formsets=PAGE_EDIT_FORMSETS,
        fieldsets=PAGE_EDIT_FIELDSET,
        combined_formset_defs=MODULE_COMBINED_FORMSET,
    )

    class Meta:
        model = get_page_model()


class PageEditBundle(bundles.VersionedObjectOnlyBundle):
    navigation = (
        ("meta", "Meta"),
        ("content_modules", "Content Modules"),
    )

    meta = views.FormView(form_class=PageForm)
    content_modules = ContentModuleBundle.as_subbundle(name="content_modules")
    main = content_modules

    class Meta:
        model = get_page_model()


class PageAddBundle(bundles.VersionedObjectOnlyBundle):
    main = views.FormView(form_class=PageForm, redirect_to_view="edit")

    class Meta:
        model = get_page_model()


class PageBundle(bundles.VersionedBundle):
    dashboard = (("main", "Page"),)

    edit = PageEditBundle.as_subbundle(name="page_edit")
    add = PageAddBundle.as_subbundle(name="page_add")

    class Meta:
        model = get_page_model()
        primary_model_bundle = True


class PagesDashboardBundle(bundles.BlankBundle):
    dashboard = (
        ("page", "Page"),
        ("carousel", "Carousel"),
    )

    page = PageBundle.as_subbundle(name="Page", title="Page", title_plural="Page")
