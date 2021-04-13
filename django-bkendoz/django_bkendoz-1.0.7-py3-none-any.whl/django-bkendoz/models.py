import json
import redis

from django.db import models
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from simple_history.models import HistoricalRecords

from .core import get_global_history_model, get_model, get_model_fields, get_history_change_model, str_list_to_str


class Style(models.Model):
    name = models.CharField(_('Style'), max_length=55)
    static_path = models.CharField(_('Chemin statique'), max_length=255)
    
    def __str__(self):
        return self.name

# GenericUser {{{1
class GenericUser(AbstractUser):
    style = models.ForeignKey(
        Style, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_("Style"))

    class Meta:
        abstract=True

    def get_absolute_url(self):
        return reverse("profile", args=[str(self.id)])

# GenericModel {{{1
class GenericModel(models.Model):
    LINK_FIELD = 'name'

    # Meta {{{2
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if hasattr(settings, 'REDIS_HOST') and hasattr(settings, 'REDIS_PORT'):
            # print('redis start updateing')
            redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
            redis_instance.delete(self.__class__._meta.label)
            model_dict = {}
            object_list = self.__class__.getAllAsOmnibarDict()
            model_dict[self.__class__._meta.label] = object_list
            redis_instance.set(self.__class__._meta.label, json.dumps(object_list))
            # print('redis updated', model_dict)
                                   

    # get_id {{{2
    @classmethod
    def get_id(cls):
        return cls.__name__.lower()

    # getAllAsOmnibarDict {{{2
    @classmethod
    def getAllAsOmnibarDict(cls):
        items = []
        for o in cls.objects.all():
            items.append({
                'type': cls._meta.verbose_name,
                'handler': 'toDetail',
                'param0': o.get_omnibar_ref(),
                'param1': o.get_absolute_url()
            })
        return items


    # get_views_struct {{{2
    @classmethod
    def get_views_struct(cls):
        assert hasattr(cls, 'views_struct'), f"GenericModel without a views dict 'views_struct' for model {cls} !"
        return cls.views_struct

    # get_view_data {{{2
    @classmethod
    def get_view_data(cls, view, prop='fields'):
        if view not in cls.get_views_struct():
            # print(f"structure pour {cls} vue : {view} non defini")
            return None
        
        if prop not in cls.get_views_struct()[view]:
            if prop == 'fields':
                return '__all__'

            if view == 'create' and prop == 'title':
                return _("Nouveau") + " " + \
                    cls._meta.verbose_name.lower()

            print(f"propriete {prop} non definie pour {cls} vue : {view}")
            return None

        return cls.get_views_struct()[view][prop]

    # get_list_menu {{{2
    @classmethod
    def get_list_menu(cls):
        views_struct = cls.get_views_struct()
        assert 'list' in views_struct, f"No list view for {cls}"
        assert 'menu' in views_struct['list'], f"No menu in listview for {cls}"

        list_menu = []
        for model_ref, view_name, faclass, url_args in views_struct['list']['menu']:
            model = get_model(model_ref)
            list_menu.append( (model.get_url(view_name.lower()), faclass) )
        return list_menu

    # get_class_menu {{{2
    @classmethod
    def get_class_menu(cls, view):
        views_struct = cls.get_views_struct()
        assert view in views_struct, f"No {view} view for {cls}"
        if 'menu' not in views_struct[view]:
            return None

        menu_tuple = views_struct[view]['menu']
        
        class_menu = []
        for menu in menu_tuple:
            model = get_model(menu[0])
            # pas de tooltip
            if len(menu) == 4:
                class_menu.append( 
                    (model.get_url(menu[1].lower()), menu[2], False )
                )
            # tooltip
            else:
                class_menu.append( 
                    (model.get_url(menu[1].lower()), menu[2], menu[4] )
                )
        return class_menu

    # # get_detail_menu {{{2
    # def get_detail_menu(self):
    #     assert 'detail' in self.__class__.get_views_struct(), f"No detail view for {self.__class__}"
    #     assert 'menu' in self.__class__.get_views_struct()['detail'], f"No detail menu for {self.__class__}"

    #     detail_menu = []

    #     for model_ref, view_name, faclass, url_args in self.__class__.get_views_struct()['detail']['menu']:

    #         module_name, class_name = model_ref.split(':')
    #         module = importlib.import_module(module_name) 
    #         model = getattr(module, class_name)

    #         kwargs = {}
    #         for self_field, other_field in url_args:
    #             if not other_field:
    #                 if not hasattr(model, self_field):
    #                     print(f"Warning : trying to acces non existent url arg {field} in {self.__class__} when generating detail menu")
    #                     continue
    #                 kwargs[self_field] = getattr(self, self_field)
    #             else:
    #                 assert hasattr(self, self_field)
    #                 assert hasattr(model, other_field)
    #                 kwargs['param'] = other_field
    #                 kwargs['pk'] = getattr(self, self_field)

    #         href = reverse_lazy(model.get_url(view_name.lower()), kwargs=kwargs)
    #         detail_menu.append( (href, faclass) )
    #     return detail_menu

    # get_view_menu {{{2
    def get_view_menu(self, view):
        assert view in self.__class__.get_views_struct(), f"No {view} view for {self.__class__}"
        if 'menu' not in self.__class__.get_views_struct()[view]:
            return None

        struct_menu = self.__class__.get_views_struct()[view]['menu'] 
        built_menu = []

        # for model_ref, view_name, faclass, url_args in struct_menu:
        for menu in struct_menu:
            model = get_model(menu[0])

            kwargs = {}
            for self_field, other_field in menu[3]:
                if not other_field:
                    if not hasattr(model, self_field):
                        print(f"Warning : trying to acces non existent url arg {field} in {self.__class__} when generating detail menu")
                        continue
                    kwargs[self_field] = getattr(self, self_field)
                else:
                    assert hasattr(self, self_field)
                    assert hasattr(model, other_field)
                    kwargs['param'] = other_field
                    kwargs['pk'] = getattr(self, self_field)

            href = reverse_lazy(model.get_url(menu[1].lower()), kwargs=kwargs)
            # pas de tooltip
            if len(menu) == 5:
                built_menu.append((href, menu[2], None, None, menu[4]))
            else:
                built_menu.append((href, menu[2], None, None, None))

        if 'extra_menu' in self.__class__.get_views_struct()[view]:
            extras = self.__class__.get_views_struct()[view]['extra_menu']
            for href, faclass, aclass, data, tooltip in extras:
                built_menu.append( (href, faclass, aclass, data, tooltip) )

        return built_menu

    # get_url {{{2
    @classmethod
    def get_url(cls, view_name):
        assert view_name in cls.get_views_struct().keys(), f"trying to reverse url with a view not specified in views_struct for {cls} with view {view_name}"
        return f"{cls._meta.app_label}:{cls.__name__.lower()}-" + view_name


    # # get_fields_data {{{2
    # @classmethod
    # def get_fields_data(cls, fieldlist):
    #     field_data = []
    #     for field in fieldlist:
    #         if not hasattr(cls, field):
    #             continue
    #         field_data.append( (field, getattr(cls, field).field.verbose_name) )
    #     print(field_data)
    #     return field_data

    # extract json dict {{{2
    @classmethod
    def extract_json_dict(cls, json):
        kwargs = {}
        for key,value in json.items():
            related_model = getattr(cls, key).field.related_model
            if related_model:
                kwargs[key] = related_model.objects.get(pk=value)
            else:
                kwargs[key] = value
        return kwargs
 
 
    # extract excel record dict {{{2
    @classmethod
    def extract_record_dict(cls, record):
        kwargs = {}
        for field in record:
            related_model = getattr(cls, field).field.related_model
            if related_model:
                kwargs[field] = related_model.objects.get(pk=record[field])
            else:
                kwargs[field] = record[field]
        return kwargs

    # create object list from excel records {{{2
    @classmethod
    def create_object_list_from_records(cls, records, fields):
        object_list = []
        index = 0
        print(records)
        print(fields)
        for record in records:
            print(record)
            o = cls(**cls.extract_record_dict(record))
            o_dict = {}
            for field in fields:
                related_model = getattr(cls, field).field.related_model
                if related_model:
                    o_dict[field] = getattr(o, field).pk
                else:
                    o_dict[field] = getattr(o, field)
            o.json = json.dumps(o_dict)
            o.index = index
            index += 1
            object_list.append(o)
        return object_list


    # get samples {{{2
    # @classmethod
    # def get_samples(cls):
    #     return [cls(), cls()]
    
    # get omnibar ref {{{2
    def get_omnibar_ref(self):
        cls = self.__class__
        f = cls.get_view_data('omnibar') 
        if f:
            return getattr(self, f)
        elif hasattr(self, 'name'):
            return self.name
        else:
            return str(self)

    # get absolute url {{{2
    def get_absolute_url(self):
        app = self.__class__._meta.app_label.lower()
        model = str(self.__class__.__name__).lower()

        if 'detail' in self.__class__.get_views_struct():
            return reverse(f"{app}:{model}-detail", args=[str(self.id)])

        if 'list' in self.__class__.get_views_struct():
            return reverse(f"{app}:{model}-list")

# GenericHistory {{{1
class GenericHistory(GenericModel):
    """
    Recense tous les changements important
    """
    ACTION_CHOICES = [
        ('ED', _("Modification")),
        ('DE', _("Suppression")),
        ('NE', _("Création")),
    ]

    action = models.CharField(
        max_length=2, choices=ACTION_CHOICES, default='ED')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    record_model = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    record_id = models.PositiveIntegerField(null=True)
    record = GenericForeignKey('record_model', 'record_id')

    date = models.DateTimeField(auto_now=True)

    views_struct = {
        'list': {
            'tpl': 'genviews/globalhistory_list.html',
            'title': _("Historique"),
            'menu': [],
            'ordering': ['-date']
        },
        'detail': {
            'tpl': 'genviews/history_changes.html',
            'menu': [],
        }
    }

    class Meta:
        abstract = True

    @classmethod
    def update(cls, action, user, m2m_changes, record):
        hist = cls(action=action, user=user, record=record)
        hist.save()
        last_change = record
        prev_change = record.prev_record
        # if not prev_change:
        #     return []
        for change in last_change.diff_against(prev_change).changes:
            f = record.instance.__class__._meta.get_field(change.field)
            if f.is_relation:
                old=f.related_model.objects.get(pk=change.old)
                new=f.related_model.objects.get(pk=change.new)
            else:
                old=change.old
                new=change.new

            hist_change = get_history_change_model()(
                field_name=change.field,
                old_value=old,
                new_value=new,
                history=hist
            )
            hist_change.save()

        for field, values in m2m_changes.items():
            old = str_list_to_str([str(v) for v in values['old']])
            new = str_list_to_str([str(v) for v in values['new']])
            hist_change = get_history_change_model()(
                field_name=field,
                old_value=old,
                new_value=new,
                history=hist
            )
            hist_change.save()


        return hist

    def get_history_changes(self):
        changes = get_history_change_model().objects.filter(history=self)
        return changes


# HistoryChange {{{1
class GenericHistoryChange(models.Model):
    """
    Stock les changements lors des mises à jour
    Ajouter l'attribut foreign key history dans la class héritée
    """
    field_name = models.CharField(max_length=255)
    old_value = models.TextField()
    new_value = models.TextField()
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.old_value:
            self.old_value = ""
        if not self.new_value:
            self.new_value = ""
        super().save(args, kwargs)


# GenericHistorizedModel {{{1
class GenericHistorizedModel(GenericModel):
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

    @property
    def hist_date(self):
        return self.history_date

    def history_create(self, user, *args, **kwargs):
        hist = get_global_history_model()(
            action='NE', 
            user=user, 
            record=self.history.first(),
        )
        hist.save()

    def history_update(self, user, m2m_changes={}, *args, **kwargs):
        hist = get_global_history_model().update(
            'ED', 
            user, 
            m2m_changes,
            self.history.first(), 
        )
        # hist.save()

    def history_delete(self, user, *args, **kwargs):
        # self.change_content += tags_delta
        self.changeReason = ""
        hist = get_global_history_model()(
            action='DE', 
            user=user, 
            record=self.history.first())
        hist.save()

# GenericExcelModel {{{1
class GenericExcelModel:
    pass
