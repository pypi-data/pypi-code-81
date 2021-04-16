# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from datetime import datetime

# Local
from .core_texts import license
from .utils import multi_replace
from .file_key import FileKey

# -------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------- Public methods -------------------------------------------------------- #

def new_license(author_name: str) -> str:
    return multi_replace(
        license,
        {
            FileKey.YEAR: datetime.utcnow().year,
            FileKey.AUTHOR_NAME: author_name
        }
    )

# -------------------------------------------------------------------------------------------------------------------------------- #