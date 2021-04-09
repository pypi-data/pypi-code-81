
from os.path import join

from pydoc import locate

from cbsettings import DjangoDefaults

from basement.assets import constants


class BasementSettings(DjangoDefaults):

    BASE_DIR = NotImplemented
    DB_NAME = NotImplemented
    DOMAIN = NotImplemented
    DEV_EMAIL = 'pmaigutyak@gmail.com'

    ROOT_URLCONF = 'core.urls'

    ALLOWED_HOSTS = ['*']

    WSGI_APPLICATION = 'core.wsgi.application'

    TIME_ZONE = 'Europe/Kiev'

    USE_TZ = True

    EMAIL_USE_TLS = True

    SITE_ID = 1

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    SILENCED_SYSTEM_CHECKS = ['mysql.E001', 'mysql.W002']

    USE_I18N = True
    USE_L10N = True

    CKEDITOR_UPLOAD_PATH = 'uploads/'

    NOCAPTCHA = True
    RECAPTCHA_PUBLIC_KEY = '6LdHaPsSAAAAAPinOxMD64UtSQtD1J37vp9qjsZw'
    RECAPTCHA_PRIVATE_KEY = '6LdHaPsSAAAAAJRHOT4Edilnp-1xSOqttWNk5dar'

    LANGUAGE_CODE = 'uk'
    LANGUAGES = (('uk', 'UA'), )

    FILE_UPLOAD_PERMISSIONS = 0o755

    THUMBNAIL_QUALITY = 85

    IS_WEBP_ENABLED = False
    IS_LESS_ENABLED = False

    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'

    STATIC_APPS = []

    STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

    STATICFILES_FINDERS = DjangoDefaults.STATICFILES_FINDERS + [
        'pipeline.finders.PipelineFinder',
        'djangobower.finders.BowerFinder'
    ]

    @property
    def BOWER_INSTALLED_APPS(self):
        return self._get_static_app_component_list(constants.BOWER_APPS_MAP)

    @property
    def STYLESHEETS(self):
        return self._get_static_app_component_list(constants.APPS_CSS_MAP)

    @property
    def JAVASCRIPT(self):
        return self._get_static_app_component_list(constants.APPS_JS_MAP)

    def _get_static_app_component_list(self, files_map):

        result = []

        for app in self.STATIC_APPS:
            try:
                styles = files_map[app]
            except KeyError:
                continue

            if isinstance(styles, str):
                result.append(styles)
            else:
                result += styles

        return tuple(result)

    @property
    def PIPELINE(self):
        return {
            'JS_COMPRESSOR': 'pipeline.compressors.jsmin.JSMinCompressor',
            'CSS_COMPRESSOR': 'pipeline.compressors.cssmin.CSSMinCompressor',
            'COMPILERS': self.COMPILERS,
            'STYLESHEETS': {
                'generic': {
                    'source_filenames': self.STYLESHEETS,
                    'output_filename': 'cache/generic.css',
                }
            },
            'JAVASCRIPT': {
                'generic': {
                    'source_filenames': self.JAVASCRIPT,
                    'output_filename': 'cache/generic.js'
                }
            }
        }

    @property
    def MEDIA_ROOT(self):
        return join(self.BASE_DIR, 'media')

    @property
    def STATIC_ROOT(self):
        return join(self.BASE_DIR, 'static-collect')

    @property
    def BOWER_COMPONENTS_ROOT(self):
        return join(self.BASE_DIR, 'static')

    @property
    def STATICFILES_DIRS(self):
        return [
            join(self.BASE_DIR, 'static'),
            join(self.BASE_DIR, 'static', 'bower_components')
        ]

    @property
    def COMPILERS(self):
        if self.IS_LESS_ENABLED:
            return ['pipeline.compilers.less.LessCompiler']
        return []

    @property
    def LOCALE_PATHS(self):
        return [join(self.BASE_DIR, 'locale')]

    @property
    def EMAIL_SUBJECT_PREFIX(self):
        return '{} |'.format(self.DOMAIN.title())

    @property
    def DEFAULT_FROM_EMAIL(self):
        return '{} <noreply@{}>'.format(self.DOMAIN.upper(), self.DOMAIN)

    @property
    def ADMINS(self):
        return ('Dev', self.DEV_EMAIL),

    @property
    def MANAGERS(self):
        return ('Dev', self.DEV_EMAIL),

    @property
    def MIDDLEWARE(self):
        return [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'pipeline.middleware.MinifyHTMLMiddleware',
            'basement.middleware.RequestEnvironmentMiddleware'
        ]

    @property
    def INSTALLED_APPS(self):

        apps = [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.sites',
            'django.contrib.sitemaps',
            'django.contrib.staticfiles',
            'basement',
            'basement.assets',
            'basement.images',
            'widget_tweaks',
            'pagination',
            'notify',
            'django_cleanup',
            'sorl.thumbnail',
            'pipeline',
            'djangobower'
        ]

        if self.USE_I18N:
            apps += ['modeltranslation']

        return apps

    @property
    def DATABASES(self):
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': self.DB_NAME,
                'USER': 'dev'
            }
        }

    @property
    def TEMPLATES(self):
        return [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': self.TEMPLATE_DIRS,
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': self.CONTEXT_PROCESSORS
            }
        }]

    @property
    def TEMPLATE_DIRS(self):
        return [
            join(self.BASE_DIR, 'templates')
        ]

    @property
    def CONTEXT_PROCESSORS(self):
        processors = [
            'django.template.context_processors.i18n',
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]

        if self.IS_WEBP_ENABLED:
            processors.append('assets.context_processors.webp')

        return processors


class LocalSettingsMixin(object):

    DEBUG = True

    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

    @property
    def EMAIL_FILE_PATH(self):
        return join(self.BASE_DIR, 'tmp')


class ProductionSettingsMixin(object):

    DEBUG = False

    EMAIL_PORT = 587
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    @property
    def STATICFILES_DIRS(self):
        return [join(self.BASE_DIR, 'static')]

    @property
    def STATIC_ROOT(self):
        return '/home/dev/sites/{}/public/static'.format(self.DOMAIN)

    @property
    def MEDIA_ROOT(self):
        return '/home/dev/sites/{}/public/media'.format(self.DOMAIN)


def settings_factory(apps):

    cleaned_apps = []

    for setting_class in apps:
        if isinstance(setting_class, str):
            located_class = locate(setting_class)

            if located_class is None:
                raise ValueError('{} not found'.format(setting_class))

            cleaned_apps.append(located_class)
        else:
            cleaned_apps.append(setting_class)

    class CommonSettings(*cleaned_apps):
        pass

    return CommonSettings
