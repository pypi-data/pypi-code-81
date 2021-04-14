from pathlib import Path

from progress.bar import Bar
from pyimporters_skos.skos import RDFFormat, SKOSOptionsModel

from pyimporters_skos_rf.skos_rf import SKOSRFKnowledgeParser


def test_xml():
    testdir = Path(__file__).parent
    source = Path(testdir,'data/LL-RF_TerminoPayeFull_20210409.zip')
    parser = SKOSRFKnowledgeParser()
    options = SKOSOptionsModel(lang="fr", rdf_format=RDFFormat.xml)
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 1808
    homme = next(c for c in concepts if c.identifier == 'https://revuefiduciaire.grouperf.com/referentiel/terme/terminologie-paye#homme')
    assert homme.identifier == 'https://revuefiduciaire.grouperf.com/referentiel/terme/terminologie-paye#homme'
    assert homme.preferredForm == 'Homme'
    assert len(homme.properties['altForms']) == 1
    assert set(homme.properties['altForms']) == set(['hommes'])
    assert homme.properties['TerminoConcept'] == "https://revuefiduciaire.grouperf.com/referentiel/concept/thesaurus-paye#homme"

