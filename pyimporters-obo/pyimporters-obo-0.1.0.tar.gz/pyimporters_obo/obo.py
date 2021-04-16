import re
from io import TextIOWrapper
from pathlib import Path
from typing import Type, Dict, Any, Generator, Union

import obonet
from collections_extended import setlist
from progress.bar import Bar
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pyimporters_plugins.base import KnowledgeParserBase, KnowledgeParserOptions, Term, maybe_archive


@dataclass
class OBOOptions(KnowledgeParserOptions):
    """
    Options for the OBO knowledge import
    """
    pass


OBOOptionsModel = OBOOptions.__pydantic_model__


class OBOKnowledgeParser(KnowledgeParserBase):
    def parse(self, source: Path, options: Union[KnowledgeParserOptions, Dict[str, Any]], bar: Bar) \
            -> Generator[Term, None, None]:
        options = OBOOptions(**options) if isinstance(options, dict) else options
        try:
            with maybe_archive(source) as file:
                g = obonet.read_obo(file)
                bar.max = len(g)
                bar.start()
                p = re.compile('^"([^"]+)" .*$')
                for id_, data in g.nodes(data=True):
                    bar.next()
                    if 'name' in data:
                        norm = data['name']
                        term: Term = Term(identifier=id_, preferredForm=norm)
                        labels = setlist()
                        props = {}
                        if 'synonym' in data:
                            for syn in data['synonym']:
                                m = p.match(syn)
                                labels.add(m.group(1))
                            props['altForms'] = list(labels)
                        wikidatas = [xref[len('Wikidata:'):] for xref in data['xref'] if xref.startswith('Wikidata:')]
                        if wikidatas:
                            props['wikidataId'] = wikidatas[0]
                        if props:
                            term.properties = props
                        yield term
        finally:
            bar.finish()

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return OBOOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OBOOptionsModel
