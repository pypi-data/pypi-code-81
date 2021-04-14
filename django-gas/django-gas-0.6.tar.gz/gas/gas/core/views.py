from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from gas.views import GASMixin


class GASLoginView(LoginView):
    template_name = "gas/login.html"

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url('gas:index')


class GASPasswordChangeView(GASMixin, PasswordChangeView):
    template_name = 'gas/base_form.html'
    success_url = reverse_lazy('gas:index')
    title = _('Change your password')
    success_message = _('Password changed.')

class Index(GASMixin, TemplateView):
    main_menu = 'index'
    template_name = "gas/index.html"
    roles = ('staff',)
