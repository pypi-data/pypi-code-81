from django.conf import settings


def react_comments_django_settings(request):
    if hasattr(settings, 'REACT_COMMENTS_DJANGO_BASE_TEMPLATE'):
        return dict(BASE_TEMPLATE=settings.REACT_COMMENTS_DJANGO_BASE_TEMPLATE)
    else:
        return dict(BASE_TEMPLATE='react-comments-django/react_index.html')
