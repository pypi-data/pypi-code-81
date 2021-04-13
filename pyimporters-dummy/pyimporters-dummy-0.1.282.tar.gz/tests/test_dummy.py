from pathlib import Path

from progress.bar import Bar
from pyimporters_plugins.base import Term

from pyimporters_dummy.dummy import DummyKnowledgeParser, DummyOptionsModel


def test_dummy():
    source = Path()
    parser = DummyKnowledgeParser()
    options = DummyOptionsModel(foo="tests")
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 1
    c0: Term = concepts[0]
    assert c0.identifier == 'tests'
    assert c0.preferredForm == 'tests'
    assert c0.properties['altForms'] == ['TESTS']
