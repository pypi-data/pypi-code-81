"""Schema for Fly Subjects
"""

import datajoint as dj

# import schema
from loris.schema.experimenters import Experimenter
from loris.schema.anatomy import CellType

# import database mixins
from loris.database.table_mixin import (
    ManualLookup, COMMENTS, PRIMARY_NAME, TAGS
)
from loris.database.attributes import chr, link, flyidentifier, crossschema, stockid
from loris.database.attributes import lookupname, tags


schema = dj.Schema('subjects')


@schema
class FlyOrigin(ManualLookup, dj.Manual):
    primary_comment = 'where is the fly from? - e.g. Bloomington, Sarah'


@schema
class FlyGenotype(dj.Manual):
    definition = f"""
    genotype_id : int auto_increment
    ---
    date_modified : date
    chr1 : <chr>
    chr2 : <chr>
    chr3 : <chr>
    chr4 = null : <chr>
    public_ids = null : <tags>
    {TAGS}
    {COMMENTS}
    """


@schema
class FlyCross(dj.Manual):
    definition = f"""
    cross_id : int auto_increment
    ---
    date_modified : date
    -> Experimenter
    cross_schema = null : <crossschema>
    -> FlyGenotype
    status = 'planned' : enum('planned', 'crossed', 'collecting', 'terminated')
    {COMMENTS}
    """


@schema
class StockGroup(ManualLookup, dj.Manual):
    primary_comment = 'stock group name - e.g. RBF'


@schema
class FlyStock(dj.Manual):
    definition = f"""
    stock_id : <stockid>  # stock id refers to the physical stock number
    ---
    -> FlyGenotype
    -> Experimenter
    date_modified : date
    status = null : enum('dead', 'missing', 'instock', 'inpersonal', 'quarantine', 'recovery')
    priority = null : enum('1', '2', '3', 'unsure', 'drop')
    -> [nullable] FlyOrigin
    -> [nullable] FlyCross
    """


@schema
class RearingMethod(ManualLookup, dj.Manual):
    primary_comment = 'how the fly was raised - e.g. 25C, darkness'


@schema
class FlySubject(dj.Manual):
    definition = f"""
    subject_id : int auto_increment
    ---
    subject_name = null : varchar(255) # custom subject name -- not necessarily unique
    -> FlyGenotype
    -> Experimenter
    -> [nullable] RearingMethod
    sex = 'U' : enum('F', 'M', 'U')
    age = null : float # age of fly in days
    prep_time = CURRENT_TIMESTAMP : timestamp # time of prep
    {TAGS}
    {COMMENTS}
    """
