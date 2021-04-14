from pathlib import Path
from typing import Type, Dict, Any, Generator, Union
from fastapi import Query
from progress.bar import Bar
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pyimporters_plugins.base import KnowledgeParserOptions, KnowledgeParserBase, Term


@dataclass
class TXTOptions(KnowledgeParserOptions):
    """
    Options for the TXT knowledge import
    """
    encoding: str = Query('utf-8', description="Encoding of the file")

TXTOptionsModel = TXTOptions.__pydantic_model__

class TXTKnowledgeParser(KnowledgeParserBase):
    def parse(self, source: Path, options: Union[BaseModel, Dict[str, Any]], bar: Bar) -> Generator[Term, None, None]:
        options = TXTOptionsModel(**options) if isinstance(options, dict) else options
        bar.max = file_len(source)
        bar.start()
        with source.open("r", encoding=options.encoding) as fin:
            for line in fin:
                bar.next()
                term = line.strip()
                if term:
                    yield Term(identifier=term, preferredForm=term)
        bar.finish()

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return TXTOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return TXTOptionsModel

def file_len(input_file:Path):
  """ Count number of lines in a file."""
  with open(input_file) as f:
      nr_of_lines = sum(1 for line in f)
  return nr_of_lines
