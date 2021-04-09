import sys

import django
from django.conf import settings
from djangoldp.tests import settings_default

settings.configure(default_settings=settings_default,
                   DJANGOLDP_PACKAGES=['djangoldp_polls', 'djangoldp_circle', 'djangoldp_conversation' 'djangoldp_polls.tests', ],
                   INSTALLED_APPS=('django.contrib.auth',
                                   'django.contrib.contenttypes',
                                   'django.contrib.sessions',
                                   'django.contrib.admin',
                                   'django.contrib.messages',
                                   'django.contrib.staticfiles',
                                   'guardian',
                                   'djangoldp_polls',
                                   'djangoldp_polls.tests',
                                   'djangoldp_circle',
                                   'djangoldp_conversation',
                                   'djangoldp',
                                   ),
                   SITE_URL='http://happy-dev.fr',
                   BASE_URL='http://happy-dev.fr',
                   REST_FRAMEWORK={
                       'DEFAULT_PAGINATION_CLASS': 'djangoldp.pagination.LDPPagination',
                       'PAGE_SIZE': 5
                   },
                   SEND_BACKLINKS=False,
                   JABBER_DEFAULT_HOST=None,
                   )

django.setup()
from django.test.runner import DiscoverRunner

test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests([
    'djangoldp_polls.tests.tests_votes',
])
if failures:
    sys.exit(failures)
