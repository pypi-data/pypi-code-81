from enum import Enum


class DocGenerationInstruction(Enum):
    allow = "allow"
    deny = "deny"
    require = "require"
