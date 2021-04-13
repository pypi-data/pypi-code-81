import unittest
from doctest import DocFileSuite

from zope.interface import Interface, directlyProvides
from zope.app.testing import ztapi, placelesssetup
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.annotation.attribute import AttributeAnnotations


from contentratings.bbb import EditorialRating
from contentratings.bbb import UserRating
from contentratings.interfaces import IEditorRatable
from contentratings.interfaces import IUserRatable
from contentratings.interfaces import IEditorialRating
from contentratings.interfaces import IUserRating
from contentratings.interfaces import IRatingType
from contentratings.interfaces import IRatingCategory
from contentratings.interfaces import IRatingManager
from contentratings.category import RatingCategoryAdapter
from contentratings.rating import Rating, NPRating
from contentratings.storage import UserRatingStorage
from contentratings.storage import EditorialRatingStorage
from contentratings.tests import checker
from contentratings.tests import SampleContainer


def baseIntegration(test):
    placelesssetup.setUp(test)
    directlyProvides(IEditorialRating, IRatingType)
    directlyProvides(IUserRating, IRatingType)
    ztapi.provideAdapter(IAttributeAnnotatable, IAnnotations,
                         AttributeAnnotations)
    ztapi.provideAdapter((IRatingCategory, Interface),
                         IRatingManager, RatingCategoryAdapter)
    container = SampleContainer()
    test.globs = {'my_container': container}


def setUpBBB(test):
    baseIntegration(test)
    ztapi.provideAdapter(IEditorRatable, IEditorialRating, EditorialRating)
    ztapi.provideAdapter(IUserRatable, IUserRating, UserRating)
    container = test.globs['my_container']
    directlyProvides(container,
                     IAttributeAnnotatable, IEditorRatable, IUserRatable)


def test_suite():
    return unittest.TestSuite((
        DocFileSuite(
            'README.rst',
            package='contentratings',
            setUp=setUpBBB,
            tearDown=placelesssetup.tearDown,
            checker=checker,
        ),
        DocFileSuite('userstorage.txt',
                     package='contentratings.tests',
                     setUp=placelesssetup.setUp,
                     tearDown=placelesssetup.tearDown,
                     globs = {'storage': UserRatingStorage}),
        DocFileSuite('editorialstorage.txt',
                     package='contentratings.tests',
                     setUp=placelesssetup.setUp,
                     tearDown=placelesssetup.tearDown,
                     globs = {'storage': EditorialRatingStorage}),
        DocFileSuite('rating.txt',
                     package='contentratings.tests',
                     setUp=placelesssetup.setUp,
                     tearDown=placelesssetup.tearDown,
                     globs = {'rating_factory': Rating}),
        DocFileSuite('rating.txt',
                     package='contentratings.tests',
                     setUp=placelesssetup.setUp,
                     tearDown=placelesssetup.tearDown,
                     globs = {'rating_factory': NPRating}),
        DocFileSuite('BBB.txt',
                     package='contentratings.tests',
                     setUp=setUpBBB,
                     tearDown=placelesssetup.tearDown,
                     globs = {'storage': EditorialRatingStorage}),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
