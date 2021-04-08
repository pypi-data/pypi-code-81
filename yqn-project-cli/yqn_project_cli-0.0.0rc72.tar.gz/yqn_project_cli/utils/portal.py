# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/2/25
from flask import (
    request,
    url_for,
    redirect,
    current_app
)
from yqn_project_cli.utils.core.as_flask import (
    UrlBase,
    BlueprintBase
)
from yqn_project_cli.utils.core.exceptions import PortalException


class PortalUrl(UrlBase):
    def __init__(self, rules, view_func=None, in_menu=True, order=0, title='', icon='', context=None, **options):
        super(PortalUrl, self).__init__(rules, view_func, title, **options)

        self.in_menu = in_menu
        self.order = order
        self.title = title if title else view_func.__name__
        self.icon = icon
        self.context = context
        self.rules = rules,
        self.view_func = view_func,
        self.options = options


class PortalNotMenuUrl(PortalUrl):
    def __init__(self, rules, view_func=None, in_menu=False, order=0, title='', icon='', context=None, **options):
        super(PortalNotMenuUrl, self).__init__(rules, view_func, in_menu, order, title, icon, context, **options)


class PortalBlueprint(BlueprintBase):
    pass


class PortalMenu:
    def __init__(self, portal_blueprints=None, title='', in_menu=True, order=0, icon='', context=None):
        self.portal_blueprints = portal_blueprints
        self.title = title
        self.in_menu = in_menu
        self.order = order
        self.icon = icon
        self.context = context


def portal_child_menus(*portal_blueprints):
    menus = []

    for blueprint in portal_blueprints:

        for url in blueprint.urls:

            if url.in_menu:
                if blueprint.url_prefix is not None:
                    _url = "/".join((blueprint.url_prefix.rstrip("/"), url.rule.lstrip("/")))

                else:
                    _url = url.rule

                menus.append({
                    'order': url.order,
                    'title': url.title,
                    'icon': url.icon,
                    'context': url.context,
                    'url': _url
                })

    return sorted(menus, key=lambda x: x['order'], reverse=True)


def portal_menu_register(*portal_menus):
    show_menus_detail = []

    for menu in [_ for _ in portal_menus if _.in_menu]:
        show_menus_detail.append(
            {
                'title': menu.title,
                'order': menu.order,
                'icon': menu.icon,
                'context': menu.context,
                'menus': portal_child_menus(*menu.portal_blueprints)
            }
        )

    return sorted(show_menus_detail, key=lambda x: x['order'], reverse=True)
