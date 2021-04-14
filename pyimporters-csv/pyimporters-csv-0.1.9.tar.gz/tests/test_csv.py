from pathlib import Path

from progress.bar import Bar
from pyimporters_plugins.base import Term

from pyimporters_csv.csv import CSVKnowledgeParser, CSVOptionsModel


def test_csv():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/Digestion.csv')
    parser = CSVKnowledgeParser()
    options = CSVOptionsModel(encoding="utf-8", identifier_col="ID",
                              preferredForm_col="prefLabel_en", altForms_cols="altLabel_en",
                              multivalue_separator="|")
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 92
    c7: Term = concepts[7]
    assert c7.identifier == 'https://opendata.inra.fr/EMTD/8'
    assert c7.preferredForm == 'specific pathogen-free animal'
    assert len(c7.properties['altForms']) == 2
    assert set(c7.properties['altForms']) == set(['SPF animal', 'specific pathogen free animal'])
