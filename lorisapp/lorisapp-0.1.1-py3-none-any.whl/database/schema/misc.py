"""miscalenous Schema
"""

import datajoint as dj

from loris.database.schema.experimenters import Experimenter
from loris.database.schema.base import ManualLookup, TAGS, COMMENTS, PRIMARY_NAME
from loris.database.attributes import lookupname, link


schema = dj.Schema('misc')


@schema
class Paper(dj.Manual):
    definition = f"""
    {PRIMARY_NAME.format(name='paper', comment='short lowercase name for paper - e.g. behnia2014a')}
    ---
    -> Experimenter
    link = null : <link>
    pdf = null : attach@attachstore
    {TAGS}
    {COMMENTS}
    bibtex_reference = null : varchar(4000)  # bibtex-style reference - check your formatting!
    """
