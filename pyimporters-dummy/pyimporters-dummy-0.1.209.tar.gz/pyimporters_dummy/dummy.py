from pathlib import Path
from typing import Type, Dict, Any, Generator, Union

from fastapi import Query
from progress.bar import Bar
from pydantic import Field, BaseModel
from pydantic.dataclasses import dataclass
from pyimporters_plugins.base import KnowledgeParserOptions, KnowledgeParserBase, Term

@dataclass
class DummyOptions(KnowledgeParserOptions):
    """
    Options for the Dummy knowledge import
    """
    foo : str = Query("bar", description="Dummy parameter")

DummyOptionsModel = DummyOptions.__pydantic_model__

class DummyKnowledgeParser(KnowledgeParserBase):
    def parse(self, source : Path, options: Union[KnowledgeParserOptions, Dict[str, Any]], bar : Bar) -> Generator[Term, None, None]:
        options = DummyOptions(**options) if isinstance(options, dict) else options
        bar.max = 1
        bar.start()
        bar.next()
        yield Term(identifier=options.foo, preferredForm=options.foo, properties={ 'altForms' : [ options.foo.upper() ] })
        bar.finish()

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return DummyOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DummyOptionsModel
