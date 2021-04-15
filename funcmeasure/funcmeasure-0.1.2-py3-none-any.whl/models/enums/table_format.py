# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from enum import Enum

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------------- enum: TableFormat ---------------------------------------------------------- #

class TableFormat(Enum):
    """Format to print the measurement data with.
    These ares the same as the 'tabulate' formats.
    For more infor check 'https://github.com/astanin/python-tabulate'
    """

    PLAIN           = 'plain'
    SIMPLE          = 'simple'
    GITHUB          = 'github'
    GRID            = 'grid'
    FANCY_GRID      = 'fancy_grid'
    PIPE            = 'pipe'
    ORGTBL          = 'orgtbl'
    JIRA            = 'jira'
    PRESTO          = 'presto'
    PRETTY          = 'pretty'
    PSQL            = 'psql'
    RST             = 'rst'
    MEDIAWIKI       = 'mediawiki'
    MOINMOIN        = 'moinmoin'
    YOUTRACK        = 'youtrack'
    HTML            = 'html'
    UNSAFEHTML      = 'unsafehtml'
    LATEX           = 'latex'
    LATEX_RAW       = 'latex_raw'
    LATEX_BOOKTABS  = 'latex_booktabs'
    LATEX_LONGTABLE = 'latex_longtable'
    TEXTILE         = 'textile'
    TSV             = 'tsv'


# ---------------------------------------------------------------------------------------------------------------------------------------- #