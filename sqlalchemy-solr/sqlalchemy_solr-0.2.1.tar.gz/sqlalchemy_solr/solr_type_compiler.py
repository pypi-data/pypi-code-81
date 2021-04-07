import re
from sqlalchemy.sql import compiler


class SolrTypeCompiler(compiler.GenericTypeCompiler):

    def visit_ARRAY(self, type_, **kw):

        inner = self.process(type_.item_type)
        return re.sub(
            r"((?: COLLATE.*)?)$",
            (
                r"%s\1"
                % (
                    "[]"
                    * (type_.dimensions if type_.dimensions is not None else 1)
                )
            ),
            inner,
            count=1,
        )
