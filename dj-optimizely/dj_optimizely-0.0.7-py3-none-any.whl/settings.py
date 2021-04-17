
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string


def get_callback_function(setting_name, default=None):
    """
    Resolve a callback function based on a setting name. 
    - If the setting value isn't set, default is returned.
    - If the setting value is already a callable function, that value is used 
    - If the setting value is a string, an attempt is made to import it. 
    
    Anything else will result in a failed import.

    """
    func = getattr(settings, setting_name, None)

    if not func:
        if not default:
            raise ImproperlyConfigured('{name} must be defined.'.format(name=setting_name))
        return default

    if callable(func):
        return func

    if isinstance(func, str):
        func = import_string(func)

    if not callable(func):
        raise ImproperlyConfigured('{name} must be callable.'.format(name=setting_name))

    return func


try:
    OPTIMIZELY_ENVIRONMENT = getattr(settings, 'OPTIMIZELY_ENVIRONMENT')
except:
    raise ImproperlyConfigured('OPTIMIZELY_ENVIRONMENT must be defined')

try:
    OPTIMIZELY_DATAFILE_URL = getattr(settings, 'OPTIMIZELY_DATAFILE_URL')
except:
    raise ImproperlyConfigured('OPTIMIZELY_DATAFILE_URL must be defined')

try:
    OPTIMIZELY_WEBHOOK_SECRET = getattr(settings, 'OPTIMIZELY_WEBHOOK_SECRET')
except:
    raise ImproperlyConfigured('OPTIMIZELY_WEBHOOK_SECRET must be defined')


def get_user_id_default(request):
    if request.user.is_authenticated:
        return request.user.pk
    else:
        return request.session._get_or_create_session_key()

get_user_id_callback = get_callback_function(
    'OPTIMIZELY_USER_ID_CALLBACK', default=get_user_id_default)


def get_user_attribs_default(request):
    attribs = {
        'is_authenticated': False,
        'is_staff': False
    }
    if request.user.is_authenticated:
        attribs['is_authenticated'] = True
        if request.user.is_staff:
            attribs['is_staff'] = True
        
    return attribs

get_user_attribs_callback = get_callback_function(
    'OPTIMIZELY_USER_ATTRIBS_CALLBACK', default=get_user_attribs_default)
