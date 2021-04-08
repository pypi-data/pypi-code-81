from dataclasses import dataclass, field
from typing import Optional

class Contact:
  first_name: str = field(default=None)
  last_name: str = field(default=None)
  phone: str = field(default=None)
  email_address: str = field(default=None)