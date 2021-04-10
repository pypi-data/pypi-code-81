from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from microsip_api.comun.sic_db import first_or_none
from django.contrib.auth.models import User


def setup_app_permissions(**kwargs):

    app_label = kwargs.get('app_label', None)
    permissions = kwargs.get('permissions', None)

    content_type_name = '{} permissions'.format(app_label)
    content_type, created = ContentType.objects.get_or_create(
        name=content_type_name,
        defaults={
            'app_label': app_label,
            'model': 'unused',
        }
    )

    for permission in permissions:
        permissionobj, created = Permission.objects.get_or_create(
            content_type=content_type,
            codename=permission['codename'],
            defaults={
                'name': permission['name'],
            }
        )
        if not created:
            permissionobj.name = permission['name']
            permissionobj.save(update_fields=['name', ])


class Permissions(object):
    """
    Clase para sacar los permisos de todas las aplicaciones installadas.
    """
    def __init__(self, *args, **kwargs):
        self.username = kwargs.get('username', None)
        self.dj_user = kwargs.get('dj_user', None)
        self.jstree_data = []
        self.permissions = {}
        for app in settings.EXTRA_MODULES:
            self.app_label = app
            self.currentparent = self.app_label.lower()
            app_name = self.app_label.replace('djmicrosip_', '').replace('django_microsip_', '').replace('django_msp_', '').upper()
            self.jstree_data.append({'id': self.app_label.lower(), 'parent': '#', 'text': app_name, })
            import importlib
            app_config = importlib.import_module('{}.config'.format(self.app_label, self.app_label))
            try:
                self.read_permisions(app_config.PERMISSIONS)
            except Exception:
                pass

    def read_permisions(self, node):
        # Si tiene nodos hijos y si no es permissions
        for node, childs in node.iteritems():
            if self.currentparent == self.app_label.lower():
                new_parentid = '{}.{}'.format(self.app_label, node.lower())
            else:
                new_parentid = '{}.{}'.format(self.currentparent, node.lower())

            if node == 'permissions':
                permissions = childs
                for permission in permissions:
                    if self.app_label in self.permissions:
                        self.permissions[self.app_label].append(permission)
                    else:
                        self.permissions[self.app_label] = [permission, ]

                    #Para mapear ids de los permisos en la base de datos
                    permission_id = permission['codename']
                    #print(self.app_label)
                    #print(permission['codename'])
                    permission_object = first_or_none(Permission.objects.filter(content_type__name=self.app_label, codename=permission['codename']))
                    if permission_object:
                        permission_id = permission_object.id
                        # print("--Permisos id-----")
                        #print(permission_id)

                    selected = False
                    if self.username and permission['codename'] != permission_id:
                        #print(self.username,permission['codename'],permission_id)
                        #print("-----------------")
                        django_user = first_or_none(User.objects.filter(username__exact=self.username))
                        dj_user=first_or_none(User.objects.filter(username__exact=self.dj_user))
                        #print(self.dj_user,"-----------------",dj_user)
                        permiso_str = '{}.{}'.format(self.app_label, permission['codename'])
                        selected = dj_user.has_perm(permiso_str)
                        print(permission_id)
                        print(permiso_str)
                        print( selected)


                    self.jstree_data.append({
                        'id': permission_id,
                        'parent': self.currentparent,
                        'text': permission['name'],
                        'state': {
                            'selected': selected,
                        }
                    })
                self.currentparent = self.app_label.lower()
            else:
                self.jstree_data.append({'id': new_parentid, 'parent': self.currentparent, 'text': node})
                self.currentparent = new_parentid
                self.read_permisions(childs)

    def setup_app_permissions(self):
        for app, permissions in self.permissions.iteritems():
            app_label = app
            content_type_name = '{} permissions'.format(app_label)
            content_type, created = ContentType.objects.get_or_create(
                name=content_type_name,
                defaults={
                    'app_label': app_label,
                    'model': 'unused',
                }
            )
            permissions_list = []
            for permission in permissions:
                permissionobj, created = Permission.objects.get_or_create(
                    content_type=content_type,
                    codename=permission['codename'],
                    defaults={
                        'name': permission['name'],
                    }
                )
                if not created:
                    permissionobj.name = permission['name']
                    permissionobj.save(update_fields=['name', ])

                permissions_list.append(permission['codename'])

            Permission.objects.filter(content_type=content_type).exclude(codename__in=permissions_list).delete()

    # def set_user_permissions(self,):
    #     for node in self.jstree_data:



    def get_permissions(self):
        return self.jstree_data
