# Make this a package
import re

from zope.interface import implementer
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.testing import renormalizing
from zope.container import sample

checker = renormalizing.RENormalizing([
    # Python 3 text has no unicode prefix, remove it from Python 2
    (re.compile("u('.*?')"), r"\1")
])


@implementer(IAttributeAnnotatable)
class SampleContainer(sample.SampleContainer):
    """An annotatable container."""

    def __repr__(self):
        # For doctests, pretend to be in a different package
        return '<zope.container.sample.SampleContainer at 0x%x>' % (
            id(self)
        )
