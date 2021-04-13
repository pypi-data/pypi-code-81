# import {{{1
import json
import redis
import pyexcel

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse, FileResponse
from django.urls import path, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .core import get_color_from_class, get_layout_data, get_model_fields, get_global_history_model, get_model, get_href
from .models import GenericModel
from .serializers import GenericUserSerializer
from .forms import get_generic_form, ImportXlsForm


# DASHBOARD {{{1
class GenericDashboardView(PermissionRequiredMixin, TemplateView):
    models = []
    template_name = 'genviews/dashboard.html'
    dflt_model_template = 'genviews/dashboard_tpl.html'
    dflt_tile_class = 'tile-simple-column'
    list_cls = 'dashboard-list'
    auth = 'superuser'

    def __init__(self, **kwargs):
        assert hasattr(settings, 'DASH_LIST_COUNT'), f"""
            DASH_LIST_COUNT non défini dans settings.py,
            il faut définir la valeur par default du nombre d'element à afficher dans le tableau de bord
            """
        self.permission_required = f'{self.auth}.dashboard'
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = {}
        for m in self.models:
            m_dict = context['models'][m] = {}
            o_cnt = m.get_view_data('dashboard', 'count') or settings.DASH_LIST_COUNT
            o_ord = m.get_view_data('dashboard', 'orderby') or None
            m_dict['title'] = m.get_view_data('dashboard', 'title')
            m_dict['class'] = m.get_view_data('dashboard', 'class') or self.dflt_tile_class
            m_dict['html'] = m.get_view_data('dashboard', 'html') or self.dflt_model_template
            m_dict['menu'] = m.get_class_menu('dashboard')
            m_dict['fields'] = self.get_dash_fields(m)
            if o_ord:
                m_dict['list'] = m.objects.all().order_by(o_ord)[:o_cnt]
            else:
                m_dict['list'] = m.objects.all()[:o_cnt]

        context['layout_data'] = get_layout_data()
        context['settings'] = settings
        return context

    def get_dash_fields(self, model):
        view_struct_fields = model.get_view_data('dashboard')
        return get_model_fields(model, view_struct_fields)


# OMNIBAR {{{1
# class GenericOmnibarView(PermissionRequiredMixin, View):
class GenericOmnibarView(View):
    models = []
    data = []
    auth = 'superuser'

    def __init__(self, **kwargs):
        self.permission_required = f'{self.auth}.omnibar'
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        items = {}
        for m in self.models:
            assert issubclass(m, GenericModel), f'''
                Pour utiliser la vue Omnibar la classe {m.get_id()} doit hériter de GenericModel' 
            '''
            items[m._meta.label] = []
            if hasattr(settings, 'REDIS_HOST') and hasattr(settings, 'REDIS_PORT'):
                redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
                model_red_value = redis_instance.get(m._meta.label)
                if model_red_value:
                    # redis_instance.delete(m._meta.label)
                    items[m._meta.label]= json.loads(model_red_value)
                else:
                    model_dict = {}
                    object_list = m.getAllAsOmnibarDict()
                    model_dict[m._meta.label] = object_list
                    redis_instance.set(m._meta.label, json.dumps(object_list))
                    items[m._meta.label] = object_list
            else:
                items[m._meta.label] = m.getAllAsOmnibarDict()
        return JsonResponse(items, safe=False)


# LIST {{{1
class GenericListView(PermissionRequiredMixin, ListView):
    template_name = 'genviews/list.html'
    template_list_name = 'genviews/table.html'
    list_cls = 'generic-list'
    fields = '__all__' 
    ordering = ['pk']

    def __init__(self, **kwargs):
        assert hasattr(settings, 'LIST_FIELDMAP'), f'''
            Pas de template LIST_FIELDMAP défini dans settings.py,
            il faut définir comment chaque field de la liste va s'afficher dans un fichier de template .html
            '''
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.list_{self.model.__name__.lower()}'
        self.template_name = self.model.get_view_data('list', 'tpl') or self.template_name
        self.ordering = self.model.get_view_data('list', 'ordering') or self.ordering
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['list_title'] = self.model.get_view_data('list', 'title')
        context['hide_search'] = self.model.get_view_data('list', 'hide_search') or False
        context['list_menu'] = self.model.get_class_menu('list')
        context['list_cls'] = self.list_cls
        context['fields'] = self._get_fields();
        context['html'] = self.model.get_view_data('list', 'html') or self.template_list_name

        context['settings'] = settings
        context['layout_data'] = get_layout_data()
        return context

    def _get_fields(self):
        fields = self.model.get_view_data('list', 'fields')
        print(fields)
        return get_model_fields(self.model, fields)


# CREATE {{{1
class GenericCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'genviews/form_view.html'
    color_classes = []

    def __init__(self, **kwargs):
        assert hasattr(settings, 'FORM_FIELDMAP'), f"""
            Pas de template FORM_FIELDMAP défini dans settings.py,
            il faut définir dans ce fichier html comment chaque field 
            particulier des formulaires vont s'afficher.
            """
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.add_{self.model.__name__.lower()}'
        self.template_name = self.model.get_view_data('create', 'html') or self.template_name

        if not self.form_class:
            self.form_class = self._create_generic_form()
            self.initial = {'model': self.model}
            # both fields and form_class not permitted
            self.fields = None
            super().__init__(**kwargs)

    def _create_generic_form(self):
        view_struct_fields = self.model.get_view_data('create')
        return get_generic_form(self.model, view_struct_fields) 

    def form_valid(self, form):
        if hasattr(self.model, 'history'):
            new_object = form.save()
            self.object = new_object
            new_object.history_create(
                self.request.user, 
            )
            return redirect(self.get_success_url())
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        if 'param' in self.kwargs and 'pk' in self.kwargs:
            self.initial = {
                self.kwargs['param']: self.kwargs['pk']
            }

        context = super().get_context_data(**kwargs)

        context['menu'] = self.model.get_class_menu('create')
        context['form_type'] = 'create'
        context['form_title'] = self.model.get_view_data('create', 'title')
        context['form_action'] = reverse_lazy(f"{self.current_app}:{self.model.__name__.lower()}-create")
        if len(self.color_classes) > 0:
            context['color_palette'] = get_color_from_class(self.color_classes)

        context['layout_data'] = get_layout_data()
        context['settings'] = settings
        return context

    def get_success_url(self):
        self.success_url = get_href(self.model.get_view_data('create', 'success_url'), self.object) or self.success_url
        if self.success_url:
            return self.success_url

        for v, args in (('detail', [self.object.pk]), ('list', None), ('create', None)):
            if self.model.get_view_data(v):
                url = f"{self.current_app}:{self.model.__name__.lower()}-{v}"
                return reverse_lazy(url, args=args)

# UPDATE {{{1
class GenericUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'genviews/form_view.html'
    color_classes = []

    def __init__(self, **kwargs):
        assert hasattr(settings, 'FORM_FIELDMAP'), f"""
            Pas de template FORM_FIELDMAP défini dans settings.py,
            il faut définir dans ce fichier html comment chaque field 
            particulier des formulaires vont s'afficher.
            """
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.change_{self.model.__name__.lower()}'
        self.template_name = self.model.get_view_data('update', 'html') or self.template_name
        if not self.form_class:
            self.form_class = self._create_generic_form()
            # fields et form_class ne peuvent etre attribues en meme temps
            self.fields = None
            self.initial = {'model': self.model}
            super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'update'
        context['form_title'] = self.model.get_view_data('update', 'title')
        context['form_action'] = reverse_lazy(
          f"{self.current_app}:{self.model.__name__.lower()}-update",
            args=[self.object.pk]
        )
        if len(self.color_classes) > 0:
            context['color_palette'] = get_color_from_class(self.color_classes)

        context['menu'] = self.object.get_view_menu('update')
        context['settings'] = settings
        context['layout_data'] = get_layout_data()
        return context

    def form_valid(self, form):
        if hasattr(self.model, 'history'):
            m2m_changes = self._compare_m2m_changes(form)
            self.object = form.save()
            self.object.history_update(
                self.request.user, 
                m2m_changes
            )
            # form.save_m2m()
            return redirect(self.get_success_url())
        return super().form_valid(form)

    def get_success_url(self):
        self.success_url = get_href(self.model.get_view_data('update', 'success_url'), self.object) or self.success_url
        if self.success_url:
            return self.success_url

        for v, args in (('detail', [self.object.pk]), ('list', None), ('create', None)):
            if self.model.get_view_data(v):
                url = f"{self.current_app}:{self.model.__name__.lower()}-{v}"
                return reverse_lazy(url, args=args)

    def _create_generic_form(self):
        view_struct_fields = self.model.get_view_data('update')
        return get_generic_form(self.model, view_struct_fields) 

    def _compare_m2m_changes(self, form):
        m2m_changes = {}
        for f in self.model._meta.get_fields():
            if f.many_to_many and not isinstance(f, models.ManyToManyRel):
                m2m_changes[f.name] = {
                    'old': set(getattr(self.object, f.name).all()),
                    'new': set(form.cleaned_data[f.name])
                }
                if m2m_changes[f.name]['old'] == m2m_changes[f.name]['new']:
                    m2m_changes.pop(f.name)
        return m2m_changes



# DETAIL {{{1
class GenericDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'genviews/detail.html'

    def __init__(self, **kwargs):
        assert hasattr(settings, 'DETAIL_FIELDMAP'), f"Pas de template DETAIL_FIELDMAP défini dans settings.py, il faut définir comment chaque field de la vue de détail va s'afficher dans un template"
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.detail_{self.model.__name__.lower()}'
        self.template_name = self.model.get_view_data('detail', 'tpl') or self.template_name
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_menu'] = self.object.get_view_menu('detail')
        context['fields'] = self._get_fields()
        context['html'] = self.model.get_view_data('detail', 'html') or None
        context['settings'] = settings
        context['MEDIA_URL'] = settings.MEDIA_URL
        context['layout_data'] = get_layout_data()
        return context

    def _get_fields(self):
        fields = self.model.get_view_data('detail', 'fields')
        if fields == '__all__':
            return None
        return fields

# HISTORY {{{1
class GenericHistoryView(PermissionRequiredMixin, DetailView):
    template_name = 'genviews/history.html'

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.history_{self.model.__name__.lower()}'
        self.template_name = self.model.get_view_data('history', 'tpl') or self.template_name
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_title'] = self.model.get_view_data('history', 'title')
        context['history_menu'] = self.object.get_view_menu('history')
        context['fields'] = self._get_fields()
        context['html'] = self.model.get_view_data('history', 'html') or None

        ct = ContentType.objects.get_for_model(self.object)
        context['history'] = get_global_history_model().objects.filter(
            record_model=ct,
            record_id=self.object.pk,
        )

        context['settings'] = settings
        context['layout_data'] = get_layout_data()
        return context

    def _get_fields(self):
        fields = self.model.get_view_data('history', 'fields')
        if fields == '__all__':
            return None
        return fields

# DELETE {{{1
class GenericDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'genviews/delete.html'

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.delete_{self.model.__name__.lower()}'
        self.template_name = self.model.get_view_data('delete', 'tpl') or self.template_name
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = f"{self.current_app}:{self.model.__name__.lower()}-detail"
        context['html'] = self.model.get_view_data('delete', 'html') or None
        context['settings'] = settings
        context['layout_data'] = get_layout_data()
        return context

    def delete(self, *args, **kwargs):
        if hasattr(self.model, 'history'):
            self.object = self.get_object()
            self.object.history_delete(self.request.user)
        return super().delete(*args, **kwargs)

    def get_success_url(self):
        for v, args in (('list', None), ('create', None)):
            if self.model.get_view_data(v):
                url = f"{self.current_app}:{self.model.__name__.lower()}-{v}"
                return reverse_lazy(url, args=args)


# EXPORT XLS {{{1
class GenericExportxlsView(PermissionRequiredMixin, View):
    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.exportxls_{self.model.__name__.lower()}'
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        if hasattr(self.model, 'get_excel_dict'):
            xls_file = pyexcel.save_as(dest_file_type="xls", adict=self.model.get_excel_dict())
            return FileResponse(xls_file, as_attachment=True,
                                    filename=f"{self.model.__name__.lower()}_export.xls")
        else: 
            tuple_fields = self.get_exportxls_fields();
            tuple_fields.reverse()
            if tuple_fields == '__all__':
                objects = self.model.objects.values()
            else:
                objects = self.model.objects.values(*tuple_fields)

            xls_file = pyexcel.save_as(dest_file_type="xls", records=objects)
            return FileResponse(xls_file, as_attachment=True,
                  filename=f"{self.model.__name__.lower()}_export.xls")

    def get_exportxls_fields(self):
        view_struct_fields = self.model.get_view_data('exportxls')
        return view_struct_fields


# IMPORT XLS {{{1
class GenericImportxlsView(PermissionRequiredMixin, FormView):
    template_name = 'genviews/import_xls.html'
    form_class = ImportXlsForm

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.importxls_{self.model.__name__.lower()}'
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f"Importer des données excel"
        context['form_subtitle'] = self.model._meta.verbose_name
        context['fields'] = self.get_import_fields()
        context['import_sample'] = self.model.get_samples()
        context['layout_data'] = get_layout_data()
        context['settings'] = settings
        return context

    def get_import_fields(self):
        view_struct_fields = self.model.get_view_data('importxls')
        return get_model_fields(self.model, view_struct_fields)

    def form_valid(self, form):
        xls_file = form.files['xls_file']
        # print(pyexcel.get_sheet(file_type='xls', file_content=xls_file))
        records = pyexcel.get_records(file_type='xls', file_content=xls_file)

        context = self.get_context_data()
        context['preview'] = True
        context['object_list'] = self.model.create_object_list_from_records(
                records, self.fields)
        context['fields'] = get_model_fields(self.model, self.fields)
        context['model_plural'] = self.model._meta.verbose_name_plural
        context['form_action'] = f"""
            {self.current_app}:{self.model.__name__.lower()}-importxlssave
        """
        return render(self.request, self.template_name, context=context)

#IMPORT XLS SAVE {{{1
class GenericImportxlssaveView(PermissionRequiredMixin, View):
    def post(self, request):
        for key, value in request.POST.items():
            if key.startswith("chk_"):
                if value == "off":
                    continue

                index = key.split("_")[1]
                data = json.loads(request.POST[index])
                m = self.model(**self.model.extract_json_dict(data))
                m.save()

        return redirect(reverse_lazy(f"{self.current_app}:{self.model.__name__.lower()}-list"))

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.importxlssave_{self.model.__name__.lower()}'
        super().__init__(**kwargs)

#   def form_valid(self, form):
#      def testinit(row):
#         # self.model.book_category.field.related_model
#         i = 0
#         new_row = []
#         for field_name in self.fields:
#            related_model = getattr(self.model, field_name).field.related_model
#            if related_model:
#               new_row.append(related_model.objects.get(pk=row[i]))
#            else:
#               new_row.append(row[i])
#            i = i + 1

#         print(new_row)
#         return new_row

#      xls_file = form.files['xls_file']
#      #print(pyexcel.get_sheet(file_type='xls', file_content=xls_file))
#      pyexcel.save_as(file_content=xls_file, file_type='xls',
#                            dest_initializer=testinit,
#                            dest_model=self.model,
#                       start_row=1,
#                       colnames=["book_category", "name"],
#                       dest_mapdict=["book_category", "name"]
#                      )

#      return super().form_valid(form)

#    def get_success_url(self):
#        if self.success_url:
#           return reverse_lazy(self.success_url)
#        else:
#           current_app = self.request.resolver_match.namespace
#           return reverse_lazy(f"{current_app}:{self.model.__name__.lower()}-importxls-preview")

##get {{{2
#   def get(self, request, *args, **kwargs):
#      if self.fields == '__all__':
#         objects = self.model.objects.values()
#      else:
#         objects = self.model.objects.values(*self.fields)

#      xls_file = pyexcel.save_as(dest_file_type="xls", records=objects)
#      response = FileResponse(xls_file, as_attachment=True,
#                              filename=f"{self.model.__name__.lower()}_import.xls")
#      return response
#      # return HttpResponse(xls_file, content_type="application/vnd.ms-excel")
#   pass

# LOGIN {{{1
class GenericLoginView(auth_views.LoginView):
    extra_context = {
        'settings': settings,
        'test': 'test'
    }

# LOGOUT {{{1
class GenericLogoutView(auth_views.LogoutView):
    extra_context = {
        'settings': settings,
        'test': 'test'
    }
# PROFILE {{{1
class GenericProfileView(PermissionRequiredMixin, UpdateView):
    template_name = 'auth/user_detail.html'
    model = get_user_model()
    fields = [
        'first_name', 'last_name', 'email', 'style'
    ]
    extra_context = {
        'settings': settings,
    }

    def __init__(self, **kwargs):
        self.current_app = self.model._meta.app_label
        self.permission_required = f'{self.current_app}.detail_{self.model.__name__.lower()}'
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = settings
        context['layout_data'] = get_layout_data()
        context['history'] = get_global_history_model().objects.filter(
            user=self.object
        )
        return context

# test flutter {{{1
class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    permission_classes = [IsAdminUser]

    def get(self, format=None):
        users = get_user_model().objects.all()
        serializer = GenericUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GenericUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

# create_model_paths {{{1
def create_model_paths(model):
    mod_name = model.__name__
    mod_name_low = mod_name.lower()
    path_to_return = []
# get_fields {{{
    def get_fields(view):
        fields = model.get_view_data(view.lower())
        if fields == '__all__':
            return get_model_fields(model)
        else:
            return fields
        if view == 'Exportxls':
            print(fields)
        return get_model_fields(model, fields)
# }}}

    assert issubclass(model, GenericModel), f"""
        {model} doit hériter de GenericModel pour pouvoir créer la structure de vues"""

    for view in model.get_views_struct().keys():
        view = view.title()
        assert globals().get(f"Generic" + view + "View"), f"""
    Erreur : aucune vue {view} définit dans la structure de vues pour Generic{view}View pour le modèle {model}.
        """
        ClassView = type(
            # name
            mod_name + view + "View", 
            # subclasses
            (globals()['Generic' + view + 'View'], ),
            # attr
            {
                "model": model,
                "fields": get_fields(view)
            }
        )

        view_path = mod_name_low + 's/' + view.lower()
        if view in ['Update', 'Detail', 'Delete', 'History']:
            view_path += '/<int:pk>'

        path_to_return.append(
            path(
                view_path,
                ClassView.as_view(),
                name=mod_name_low + '-' + view.lower()
            )
        )

        if view == 'Create': 
            view_path += '/<str:param>/<int:pk>'
            path_to_return.append(
                path(
                    view_path,
                    ClassView.as_view(),
                    name=mod_name_low + '-' + view.lower()
                )
            )

    return path_to_return
