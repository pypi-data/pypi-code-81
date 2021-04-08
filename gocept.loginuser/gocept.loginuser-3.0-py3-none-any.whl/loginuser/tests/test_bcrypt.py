# Run AuthEncoding tests against our BCrypt implementation
from AuthEncoding.tests.test_AuthEncoding import testBadPassword  # noqa
from AuthEncoding.tests.test_AuthEncoding import testBlankPassword  # noqa
from AuthEncoding.tests.test_AuthEncoding import testGoodPassword  # noqa
from AuthEncoding.tests.test_AuthEncoding import testLongPassword  # noqa
from AuthEncoding.tests.test_AuthEncoding import testShortPassword  # noqa
import AuthEncoding


def test_bcrypt__BCryptScheme__1():
    """BCryptScheme is registered in AuthEncoding."""
    assert 'BCRYPT' in AuthEncoding.listSchemes()
