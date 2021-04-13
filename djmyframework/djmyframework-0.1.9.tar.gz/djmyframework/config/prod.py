# -*- coding: utf-8 -*-
# @Time    : 2019-08-28 16:20
# @Author  : xzr
# @File    : __init__
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 正式环境 settings 基本设置


# SECURITY WARNING: don't run with debug turned on in production!

import logging

DEBUG = False

from django.conf import settings

logging.info('This env is production,DEBUG = False')
logging.info('BASE_DIR: %s' % settings.BASE_DIR)

DATABASES = {
        'default': {
                'ENGINE'  : 'django.db.backends.mysql',

                'NAME'    : 'djmyadmin',
                'USER'    : 'root',
                'PASSWORD': '123456',
                'HOST'    : '10.19.200.185',

                'PORT'    : '3306',

                'OPTIONS' : {'isolation_level': None}
        },
        'read'   : {

                'ENGINE'  : 'django.db.backends.mysql',

                'NAME'    : 'djmyadmin',
                'USER'    : 'root',
                'PASSWORD': '123456',
                'HOST'    : '10.19.200.185',

                'PORT'    : '3306',
                'OPTIONS' : {'isolation_level': None}
        },
        'write'  : {

                'ENGINE'  : 'django.db.backends.mysql',
                'NAME'    : 'djmyadmin',
                'USER'    : 'root',
                'PASSWORD': '123456',
                'HOST'    : '10.19.200.185',
                'PORT'    : '3306',
                'OPTIONS' : {'isolation_level': None}

        }

}
DATABASES['read'] = DATABASES['default']
DATABASES['write'] = DATABASES['default']
DATABASES['db'] = DATABASES['default']


#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://:123456@10.19.200.185:6379/2",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

CELERY_BROKER_URL = 'redis://:123456@h29:6379/1'

CHANNEL_LAYERS = {
        "default": {
                "BACKEND": "channels_redis.core.RedisChannelLayer",
                "CONFIG" : {
                        "hosts": ["redis://:123456@h29:6379/2"],
                },
        },
}

AUTH_LDAP_SERVER_URI = "ldap://ldap.example.com"