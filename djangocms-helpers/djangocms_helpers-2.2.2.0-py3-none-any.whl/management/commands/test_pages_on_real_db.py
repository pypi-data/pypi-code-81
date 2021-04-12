import unittest

from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        from djangocms_helpers.tests.test_pages import PagesTestCase
        
        suite = unittest.TestLoader().loadTestsFromTestCase(PagesTestCase)
        unittest.TextTestRunner().run(suite)
