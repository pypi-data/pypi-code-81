from pathlib import Path

from progress.bar import Bar
from pyimporters_plugins.base import Term

from pyimporters_csv.text import TXTKnowledgeParser, TXTOptionsModel


def test_text():
    source = Path('data/currencies.txt')
    parser = TXTKnowledgeParser()
    options = TXTOptionsModel(encoding="utf-8")
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 279
    c1 : Term = concepts[1]
    assert c1.identifier == 'Euro'
    assert c1.preferredForm == 'Euro'
    assert c1.properties is None
