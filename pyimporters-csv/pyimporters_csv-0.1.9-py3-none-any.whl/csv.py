from collections import defaultdict
from pathlib import Path
from typing import Type, Dict, Any, Generator, Optional, Union
import pandas as pd
from fastapi import Query
from progress.bar import Bar
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pyimporters_plugins.base import KnowledgeParserBase, Term, KnowledgeParserOptions

from pyimporters_csv.text import file_len, TXTOptions


@dataclass
class CSVOptions(TXTOptions):
    """
    Options for the CSV knowledge import
    """
    separator: str = Query(',', description="Field separator")
    quotechar: str = Query('"', description="")
    multivalue_separator: str = Query("|",
                                      description="Additional separator to split multivalued columns if any")
    header: Optional[int] = Query(0,
                                  description="""Row number (0-indexed) to use as the column names,
                                  leave blank if there is no header""")
    identifier_col: str = Query("identifier",
                                description="""Column to use as the identifier of the concept,
                                either given as string name or column index""")
    preferredForm_col: str = Query("preferredForm",
                                   description="""Column to use as the preferred form of the term,
                                   either given as string name or column index""")
    altForms_cols: str = Query("altForms",
                               description="""Column(s) to use as the alternative forms of the term,
                               either given as a (list of) string name(s) or column index(es)""")


CSVOptionsModel = CSVOptions.__pydantic_model__


class CSVKnowledgeParser(KnowledgeParserBase):
    def parse(self, source: Path, options: Union[BaseModel, Dict[str, Any]], bar: Bar) -> Generator[Term, None, None]:
        options: CSVOptionsModel = CSVOptionsModel(**options) if isinstance(options, dict) else options
        bar.max = file_len(source)
        bar.start()
        lines = pd.read_csv(source,
                            sep=options.separator,
                            quotechar=options.quotechar,
                            header=options.header,
                            encoding=options.encoding).fillna(value='')
        prefLabel_col = 0\
            if (options.preferredForm_col is None or not options.preferredForm_col.strip())\
            else col_index(options.preferredForm_col)
        identifier_col = prefLabel_col\
            if (options.identifier_col is None or not options.identifier_col.strip())\
            else col_index(options.identifier_col)
        altLabel_cols = None\
            if (options.altForms_cols is None or not options.altForms_cols.strip())\
            else options.altForms_cols
        all_cols = [col for col in lines.columns if
                    col not in [prefLabel_col, identifier_col]] if altLabel_cols else None
        for index, row in lines.iterrows():
            bar.next()
            prefLabel = row[prefLabel_col].strip()
            identifier = row[identifier_col].strip()
            concept: Term = Term(identifier=identifier, preferredForm=prefLabel)
            if altLabel_cols:
                concept.properties = defaultdict(list)
                alts_cols = [col_index(x.strip()) for x in altLabel_cols.split(',')]
                restrict = any(col.startswith("-") for col in alts_cols)
                if restrict:
                    list_cols = [col for col in all_cols if f"-{col}" not in alts_cols]
                    alts_cols = list_cols
                for alt_col in alts_cols:
                    altLabel = row[alt_col].strip()
                    if altLabel:
                        if options.multivalue_separator:
                            altLabels = [x.strip() for x in altLabel.split(options.multivalue_separator)]
                            concept.properties['altForms'].extend(altLabels)
                        else:
                            concept.properties['altForms'].append(altLabel)
            yield concept
        bar.finish()

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return CSVOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return CSVOptionsModel


def header_index(col):
    return int(col) if col.lstrip('+-').isdigit() else None


def col_index(col):
    return int(col) if col.lstrip('+-').isdigit() else col
