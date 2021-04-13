# -*- coding: utf-8 -*-
# @Time    : 2020-07-16 14:25
# @Author  : xzr
# @File    : settings
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :


AUTH_USER_MODEL = 'myadmin.models.user.User'

USE_LDAP_AUTH = True
LDAP_HOST = 'ldaps://127.0.0.1:13891'
LDAP_BASE_DN = 'dc=bigdata,dc=com'

LDAP_BIND_DN = "cn=bigdata,ou=people,%s" % LDAP_BASE_DN
LDAP_BIND_PASSWORD = "123"

LDAP_USER_BASE_DN = "ou=people,%s" % LDAP_BASE_DN
LDAP_USER_FILTER = '(objectClass=posixAccount)'

LDAP_GROUP_BASE_DN = "ou=role,%s" % LDAP_BASE_DN
LDAP_GROUP_FILTER = '(objectClass=posixGroup)'

LDAP_USER_ATTR_MAP = {
        "alias": "alias",
        "cn" : "name",
        "email": "email",
}

LDAP_GROUP_ATTR_MAP = {
        "alias": "alias",
        "name" : "cn",
}


class SMS_CONFIG:
    AppKey = '1400029142'
    AppSecret = '122424d328d272fa85cc01d874fa5066'
    sms_free_sign_name = "游娱"
    sms_template_code = "16858"
