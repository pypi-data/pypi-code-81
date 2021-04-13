# Create your tests here.
import json

from django.conf import settings
from django.test import RequestFactory, TestCase



class BaseTestCase(TestCase):

    def setUp(self):
        settings.DEBUG = True
        self.factory = RequestFactory()

