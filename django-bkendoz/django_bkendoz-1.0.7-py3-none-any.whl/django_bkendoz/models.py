from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from simple_history.models import HistoricalRecords

from .core import (
    get_global_history_model,
    get_model,
    get_history_change_model,
    str_list_to_str,
)


class GenericStyle(models.Model):
    """Classe abstraite générique représentant un fichier de style CSS"""

    name = models.CharField(_("Style"), max_length=55)
    static_path = models.CharField(_("Chemin statique du style"), max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class GenericUser(AbstractUser):
    """Classe abstraite générique représentant un utilisateur"""

    # style = models.ForeignKey(
    #     settings.STYLE_MODEL, on_delete=models.CASCADE, null=True, blank=True,
    #     verbose_name=_("Style"))

    class Meta:
        abstract = True

    def get_absolute_url(self):
        """Retourne un lien vers le profile de l'utilisateur"""
        return reverse("profile", args=[str(self.id)])

    def to_datatable(self):
        """Retourne la vue pour l'affichage de l'utilisateur dans
        les 'datatable'
        """
        return f'<a href="{self.get_absolute_url()}">{str(self)}</a>'


class GenericModel(models.Model):
    """Classe abstraite générique dont peuvent hériter des modèles pour
    bénéficier de la génération automatique des vues django_bkendoz
    """

    # LINK_FIELD = "name"
    name = models.CharField(_("Nom"), max_length=255, default="")
    views_struct = {}

    class Meta:
        abstract = True
        verbose_name = "GenericModel"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete("omnibar:" + self.__class__.__name__)
        cache.delete_pattern(self.__class__.__name__ + ":viewset:*:*")
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Renvoie un lien vers une vue dans l'ordre suivant :
        * detail
        * datatable
        * list
        * sinon str vide

        Returns:
            str: href
        """
        app = self.__class__._meta.app_label.lower()
        model = str(self.__class__.__name__).lower()

        if "detail" in self.__class__.get_views_struct():
            return reverse(f"{app}:{model}-detail", args=[str(self.id)])

        if "datatable" in self.__class__.get_views_struct():
            return reverse(f"{app}:{model}-datatable")

        if "list" in self.__class__.get_views_struct():
            return reverse(f"{app}:{model}-list")

        return ""

    def to_datatable(self):
        """Retourne la vue pour l'affichage de l'instance du modèle
        dans les 'datatable'"""

        return f'<a href="{self.get_absolute_url()}">{str(self)}</a>'

    @classmethod
    def href_to_datalist(cls):
        """Retourne un lien vers l'affichage en liste du modèle"""

        verbose_name = cls._meta.verbose_name
        if "datatable" in cls.get_views_struct():
            path_name = cls.get_url("datatable")
        elif "list" in cls.get_views_struct():
            path_name = cls.get_url("list")
        else:
            return verbose_name

        return f'<a href="{reverse(path_name)}">{verbose_name}</a>'

    @classmethod
    def to_omnibar_dict(cls, qs=None):
        """Export des objets d'un modèle pour l'omnibar avec
        type, handler, param0, param1
        """

        qs = qs or cls.objects.all()
        items = []
        for obj in qs:
            items.append(
                {
                    "type": cls._meta.verbose_name,
                    "handler": "toDetail",
                    "param0": obj.get_omnibar_ref(),
                    "param1": obj.get_absolute_url(),
                }
            )
        return items

    def get_omnibar_ref(self):
        """Retourne une référence pour l'affichage dans l'omnibar, dans
        l'ordre de priorité :
        * omnibar
        * référence
        * name
        * str(self)
        """

        cls = self.__class__
        omnibar_ref = cls.get_view_data("omnibar")
        if omnibar_ref and hasattr(self, omnibar_ref):
            return getattr(self, omnibar_ref)
        elif hasattr(self, "reference"):
            return getattr(self, "reference")
        elif hasattr(self, "name"):
            return self.name
        else:
            return str(self)

    @classmethod
    def get_views_struct(cls):
        """Retourne la structure de vue du modèle."""

        return cls.views_struct

    @classmethod
    def get_view_data(cls, view, prop="fields"):
        """Retourne les données de la vue"""

        if view not in cls.get_views_struct():
            # print(f"structure pour {cls} vue : {view} non defini")
            return None

        if prop not in cls.get_views_struct()[view]:
            if prop == "fields":
                return "__all__"

            if view == "create" and prop == "title":
                return _("Nouveau") + " " + cls._meta.verbose_name.lower()

            # print(f"propriete {prop} non definie pour {cls} vue : {view}")
            return None

        return cls.get_views_struct()[view][prop]

    @classmethod
    def get_list_menu(cls):
        views_struct = cls.get_views_struct()
        assert "list" in views_struct, f"No list view for {cls}"
        assert "menu" in views_struct["list"], f"No menu in listview for {cls}"

        list_menu = []
        for model_ref, view_name, faclass, _ in views_struct["list"]["menu"]:
            model = get_model(model_ref)
            list_menu.append((model.get_url(view_name.lower()), faclass))
        return list_menu

    @classmethod
    def get_class_menu(cls, view):
        views_struct = cls.get_views_struct()
        assert view in views_struct, f"No {view} view for {cls}"
        if "menu" not in views_struct[view]:
            return None

        menu_tuple = views_struct[view]["menu"]

        class_menu = []
        for menu in menu_tuple:
            model = get_model(menu[0])
            # pas de tooltip
            if len(menu) == 4:
                class_menu.append((model.get_url(menu[1].lower()), menu[2], False))
            # tooltip
            else:
                class_menu.append((model.get_url(menu[1].lower()), menu[2], menu[4]))

        if "extra_menu" in views_struct[view]:
            extras = views_struct[view]["extra_menu"]
            for url, faclass, _, _, tooltip in extras:
                # i = 0
                # if url:
                # href = reverse_lazy(url)
                # else:
                # href = "#"
                class_menu.append((url, faclass, tooltip))

        return class_menu

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

    def get_view_menu(self, view):
        assert (
            view in self.__class__.get_views_struct()
        ), f"No {view} view for {self.__class__}"
        if "menu" not in self.__class__.get_views_struct()[view]:
            return None

        struct_menu = self.__class__.get_views_struct()[view]["menu"]
        built_menu = []

        # for model_ref, view_name, faclass, url_args in struct_menu:
        for menu in struct_menu:
            model = get_model(menu[0])

            kwargs = {}
            i = 0
            for self_field, other_field in menu[3]:
                if not other_field:
                    if not hasattr(model, self_field):
                        print(
                            f"Warning : trying to acces non existent url arg {self_field} or {other_field} in {self.__class__} when generating detail menu"
                        )
                        continue
                    kwargs[self_field] = getattr(self, self_field)
                else:
                    assert hasattr(self, self_field)
                    assert hasattr(model, other_field)
                    kwargs["param" + str(i)] = other_field
                    kwargs["pk" + str(i)] = getattr(self, self_field)
                i = i + 1

            href = reverse_lazy(model.get_url(menu[1].lower()), kwargs=kwargs)
            # pas de tooltip
            if len(menu) == 5:
                built_menu.append((href, menu[2], None, None, menu[4]))
            else:
                built_menu.append((href, menu[2], None, None, None))

        if "extra_menu" in self.__class__.get_views_struct()[view]:
            extras = self.__class__.get_views_struct()[view]["extra_menu"]
            for url, url_args, faclass, aclass, data, tooltip in extras:

                kwargs = {}
                i = 0
                for self_field, other_field in url_args:
                    if not other_field:
                        if not hasattr(model, self_field):
                            print(
                                f"Warning : trying to acces non existent url arg {self_field} or {other_field} in {self.__class__} when generating detail menu"
                            )
                            continue
                        kwargs[self_field] = getattr(self, self_field)
                    else:
                        assert hasattr(self, self_field)
                        assert hasattr(model, other_field)
                        kwargs["param" + str(i)] = other_field
                        kwargs["pk" + str(i)] = getattr(self, self_field)
                    i = i + 1

                if url:
                    href = reverse_lazy(url, kwargs=kwargs)
                else:
                    href = "#"
                built_menu.append((href, faclass, aclass, data, tooltip))

        return built_menu

    @classmethod
    def get_url(cls, view_name):
        assert (
            view_name in cls.get_views_struct().keys()
        ), f"trying to reverse url with a view not specified in views_struct for {cls} with view {view_name}"
        return f"{cls._meta.app_label}:{cls.__name__.lower()}-" + view_name

    # @classmethod
    # def get_fields_data(cls, fieldlist):
    #     field_data = []
    #     for field in fieldlist:
    #         if not hasattr(cls, field):
    #             continue
    #         field_data.append( (field, getattr(cls, field).field.verbose_name) )
    #     print(field_data)
    #     return field_data

    @classmethod
    def extract_json_dict(cls, json):
        kwargs = {}
        for key, value in json.items():
            related_model = getattr(cls, key).field.related_model
            if related_model:
                kwargs[key] = related_model.objects.get(pk=value)
            else:
                kwargs[key] = value
        return kwargs

    @classmethod
    def extract_record_dict(cls, record):
        kwargs = {}
        for field in record:
            splitted_field = field.split("__")
            if len(splitted_field) > 1:
                model_name = splitted_field[0]
                # model_field = splitted_field[1]
                related_model = getattr(cls, model_name).field.related_model
                obj, _ = related_model.objects.get_or_create(name=record[field])
                kwargs[model_name] = obj
            else:
                kwargs[field] = record[field]
        print(kwargs)
        return kwargs

    #     @classmethod
    #     def extract_record_dict(cls, record):
    #         kwargs = {}
    #         for field in record:
    #             related_model = getattr(cls, field).field.related_model
    #             if related_model:
    #                 kwargs[field] = related_model.objects.get(pk=record[field])
    #             else:
    #                 kwargs[field] = record[field]
    #         return kwargs

    @classmethod
    def create_object_list_from_records(cls, records):
        object_list = []
        # index = 0
        # print(fields)
        for record in records:
            # print(record)
            o = cls(**cls.extract_record_dict(record))
            o.save()
            # o_dict = {}
            # for field in fields:
            #     related_model = getattr(cls, field).field.related_model
            #     print(related_model)
            #     if related_model:
            #         o_dict[field] = getattr(o, field).pk
            #     else:
            #         o_dict[field] = getattr(o, field)
            # o.json = json.dumps(o_dict)
            # o.index = index
            # index += 1
            object_list.append(o)
        return object_list

    # @classmethod
    # def get_samples(cls):
    #     return [cls(), cls()]
    # @classmethod
    # def get_omnibar_qs(cls):
    #     return cls.objects.all()

    # @classmethod
    # def get_id(cls):
    #     return cls.__name__.lower()


class GenericHistory(GenericModel):
    """
    Recense tous les changements important
    """

    ACTION_CHOICES = [
        ("ED", _("Modification")),
        ("DE", _("Suppression")),
        ("NE", _("Création")),
    ]

    action = models.CharField(max_length=2, choices=ACTION_CHOICES, default="ED")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, related_name="global_history"
    )
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    record_name = models.CharField(max_length=255, null=True, blank=True)
    model_verbose_name = models.CharField(max_length=255, null=True, blank=True)

    date = models.DateTimeField(auto_now=True)

    views_struct = {
        "datatable": {
            "title": _("Historique"),
            "menu": [],
            "ordering": ["-date"],
            "fields": [
                ("action", "action", "Action"),
                ("date", "date", "Date"),
                ("user_link", "user.username", "Utilisateur"),
                ("record_link", "record_name", "Objet"),
                ("model_list_link", "model_verbose_name", "Type"),
            ],
            "api_url": "api/globalhistory",
            "css_modal_id": "modal-changes",
        },
        # 'list': {
        #     'tpl': 'django_bkendoz/globalhistory_list.html',
        #     'title': _("Historique"),
        #     'menu': [],
        #     'ordering': ['-date']
        # },
        "detail": {
            "tpl": "django_bkendoz/history_changes.html",
            "menu": [],
        },
    }

    class Meta:
        abstract = True

    @classmethod
    def update(cls, action, user, m2m_changes, content_object):
        hist = cls(
            action=action,
            user=user,
            content_object=content_object,
            record_name=str(content_object.instance),
            model_verbose_name=content_object.instance.__class__._meta.verbose_name,
        )
        hist.save()

        last_change = content_object
        prev_change = content_object.prev_record
        # if not prev_change:
        #     return []
        for change in last_change.diff_against(prev_change).changes:
            f = content_object.instance.__class__._meta.get_field(change.field)
            if f.is_relation:
                if change.old:
                    old = f.related_model.objects.get(pk=change.old)
                else:
                    old = None
                new = f.related_model.objects.get(pk=change.new)
            else:
                old = change.old
                new = change.new

            hist_change = get_history_change_model()(
                field_name=change.field, old_value=old, new_value=new, history=hist
            )
            hist_change.save()

        for field, values in m2m_changes.items():
            old = str_list_to_str([str(v) for v in values["old"]])
            new = str_list_to_str([str(v) for v in values["new"]])
            hist_change = get_history_change_model()(
                field_name=field, old_value=old, new_value=new, history=hist
            )
            hist_change.save()

        return hist

    def get_history_changes(self):
        changes = get_history_change_model().objects.filter(history=self)
        return changes


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


class GenericHistorizedModel(GenericModel):
    # history_date = None
    # history_object
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        # self.history_date = None
        # self.history = None
        super().__init__(*args, **kwargs)

    @property
    def hist_date(self):
        return self.history_date

    def history_create(self, user, *args, **kwargs):
        content_object = self.history.first()
        hist = get_global_history_model()(
            action="NE",
            user=user,
            content_object=content_object,
            record_name=str(content_object.instance),
            model_verbose_name=content_object.instance.__class__._meta.verbose_name,
        )
        hist.save()

    def history_update(self, user, m2m_changes=None):
        content_object = self.history.first()
        get_global_history_model().update(
            "ED",
            user,
            m2m_changes,
            content_object,
        )
        # hist.save()

    def history_delete(self, user, *args, **kwargs):
        content_object = self.history.first()
        hist = get_global_history_model()(
            action="DE",
            user=user,
            content_object=content_object,
            record_name=str(content_object.instance),
            model_verbose_name=content_object.instance.__class__._meta.verbose_name,
        )
        hist.save()


class GenericExcelModel:
    pass
