from typing import Optional
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ShareInstruction:
    free: bool = True
    price: Optional[Decimal] = None
    currency: str = "$"
