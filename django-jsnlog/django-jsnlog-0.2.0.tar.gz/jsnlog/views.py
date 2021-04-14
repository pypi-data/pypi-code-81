# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import View

from django.apps import apps


@method_decorator(ensure_csrf_cookie, name='post')
class JSNLogView(View):

    def post(self, request):
        app_config = apps.get_app_config('jsnlog')
        logger = app_config.logger

        log = json.loads(request.body)
        logger.error(f'user={request.user} error={log}')
        return HttpResponse(status=200)
