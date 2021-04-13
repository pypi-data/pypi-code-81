import unittest
import doctest as doctestunit


from zope.interface import Interface, directlyProvides
from zope.container.sample import SampleContainer
from zope.app.testing import ztapi
from zope.component.testing import setUp, tearDown
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.annotation.attribute import AttributeAnnotations
from zope.testing.renormalizing import IGNORE_EXCEPTION_MODULE_IN_PYTHON2


from contentratings.interfaces import IRatingCategory
from contentratings.interfaces import IRatingManager
from contentratings.category import RatingCategoryAdapter
from contentratings.tests import checker


class DummyView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        if self.context.can_read:
            return "%s on: %s (%s)"%(self.__class__.__name__,
                                     self.context.title, self.context.name)
        return '  \n\n'  # a blank entry, should be ignored


def setUpViewTests(test):
    setUp(test)
    # Setup our adapter from category to rating api
    ztapi.provideAdapter((IRatingCategory, Interface),
                         IRatingManager, RatingCategoryAdapter)
    ztapi.provideAdapter(IAttributeAnnotatable, IAnnotations,
                         AttributeAnnotations)
    container = SampleContainer()
    directlyProvides(container, IAttributeAnnotatable)
    test.globs = {'my_container': container}


def test_suite():
    return unittest.TestSuite((
        doctestunit.DocFileSuite(
            'aggregator.txt',
            package='contentratings.browser',
            setUp=setUpViewTests,
            tearDown=tearDown,
            checker=checker,
        ),
        doctestunit.DocTestSuite(
            'contentratings.browser.traverser',
            setUp=setUpViewTests,
            tearDown=tearDown,
            checker=checker,
            optionflags=(
                doctestunit.ELLIPSIS
                | IGNORE_EXCEPTION_MODULE_IN_PYTHON2
                | doctestunit.IGNORE_EXCEPTION_DETAIL
            ),
        ),
        doctestunit.DocTestSuite(
            'contentratings.browser.utils',
            setUp=setUp,
            tearDown=tearDown,
            checker=checker,
        ),
        doctestunit.DocFileSuite(
            'views.txt',
            package='contentratings.browser',
            setUp=setUpViewTests,
            tearDown=tearDown,
            checker=checker,
            optionflags=(
                doctestunit.ELLIPSIS
                | IGNORE_EXCEPTION_MODULE_IN_PYTHON2
                | doctestunit.IGNORE_EXCEPTION_DETAIL
            )
        ),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
