from dataclasses import dataclass
from .DocGenerationInstruction import DocGenerationInstruction


@dataclass
class PartShareInstruction:
    href: int
    include: DocGenerationInstruction
