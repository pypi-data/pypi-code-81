from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Type, Dict, Any, Generator, Union

from fastapi import Query
from progress.bar import Bar
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pyimporters_plugins.base import KnowledgeParserBase, KnowledgeParserOptions, Term
from rdflib import Graph, RDF, SKOS
from rdflib.resource import Resource


class RDFFormat(str, Enum):
    xml = 'xml'
    n3 = 'n3'
    turtle = 'turtle'
    nt = 'nt'
    json_ld = 'json-ld'


@dataclass
class SKOSOptions(KnowledgeParserOptions):
    """
    Options for the RDF knowledge import
    """
    rdf_format: RDFFormat = Query(RDFFormat.xml, description="RDF format")


SKOSOptionsModel = SKOSOptions.__pydantic_model__


class SKOSKnowledgeParser(KnowledgeParserBase):
    def parse(self, source: Path, options: Union[KnowledgeParserOptions, Dict[str, Any]], bar: Bar) \
            -> Generator[Term, None, None]:
        options = SKOSOptions(**options) if isinstance(options, dict) else options
        bar.max = 20
        bar.start()
        g = Graph()
        thes = g.parse(source=str(source), format=options.rdf_format)
        bar.next(20)
        bar.max = len(list(thes.subjects(predicate=RDF.type, object=SKOS.Concept)))
        for curi in thes[:RDF.type:SKOS.Concept]:
            bar.next()
            c = Resource(g, curi)
            concept: Term = None
            for prefLabel in c.objects(SKOS.prefLabel):
                if prefLabel.language.startswith(options.lang):
                    concept: Term = Term(identifier=str(curi), preferredForm=prefLabel.value)
            if concept:
                props = defaultdict(list)
                for altLabel in c.objects(SKOS.altLabel):
                    if altLabel.language.startswith(options.lang):
                        props['altForms'].append(altLabel.value)
                if props:
                    concept.properties = props
                yield concept
        bar.finish()

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return SKOSOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SKOSOptionsModel
