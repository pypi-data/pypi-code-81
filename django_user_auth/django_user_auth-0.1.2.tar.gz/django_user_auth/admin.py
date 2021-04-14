from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class EXUserAdmin(UserAdmin):
    """
    增加了mobile,是否域用户的显示
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {
         'fields': ('first_name', 'last_name', 'email', 'mobile')}),
        (('Permissions'), {
         'fields': ('is_active', 'is_ad_account', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, EXUserAdmin)
