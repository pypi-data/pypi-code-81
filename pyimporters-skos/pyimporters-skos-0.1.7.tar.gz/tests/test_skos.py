from pathlib import Path

from progress.bar import Bar
from pyimporters_plugins.base import Term

from pyimporters_skos.skos import SKOSKnowledgeParser, RDFFormat, SKOSOptionsModel


def test_xml():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/test.rdf')
    parser = SKOSKnowledgeParser()
    options = SKOSOptionsModel(rdf_format=RDFFormat.xml)
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 1
    c0: Term = concepts[0]
    assert c0.identifier == 'http://skos.um.es/unescothes/C02796'
    assert c0.preferredForm == 'Occupations'
    assert len(c0.properties['altForms']) == 4
    assert set(c0.properties['altForms']) == set(['Professional occupations', 'Jobs', 'Careers', 'Professions'])


def test_n3():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/test.n3')
    parser = SKOSKnowledgeParser()
    options = SKOSOptionsModel(rdf_format=RDFFormat.n3)
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 1
    c0: Term = concepts[0]
    assert c0.identifier == 'http://skos.um.es/unescothes/C02796'
    assert c0.preferredForm == 'Occupations'
    assert len(c0.properties['altForms']) == 4
    assert set(c0.properties['altForms']) == set(['Professional occupations', 'Jobs', 'Careers', 'Professions'])


def test_nt():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/test.nt')
    parser = SKOSKnowledgeParser()
    options = SKOSOptionsModel(rdf_format=RDFFormat.nt)
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 1
    c0: Term = concepts[0]
    assert c0.identifier == 'http://skos.um.es/unescothes/C02796'
    assert c0.preferredForm == 'Occupations'
    assert len(c0.properties['altForms']) == 4
    assert set(c0.properties['altForms']) == set(['Professional occupations', 'Jobs', 'Careers', 'Professions'])


def test_jsonld():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/test.jsonld')
    parser = SKOSKnowledgeParser()
    options = SKOSOptionsModel(rdf_format=RDFFormat.json_ld)
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 1
    c0: Term = concepts[0]
    assert c0.identifier == 'http://skos.um.es/unescothes/C02796'
    assert c0.preferredForm == 'Occupations'
    assert len(c0.properties['altForms']) == 4
    assert set(c0.properties['altForms']) == set(['Professional occupations', 'Jobs', 'Careers', 'Professions'])
