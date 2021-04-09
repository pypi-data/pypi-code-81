__all__ = [
    "YAML",
    "CommentedMap",
    "CommentedSeq",
    "CommentedSet",
    "CommentedOrderedMap",
    "CommentedBase",
    "Tag",
    "TaggedScalar",
]

try:
    from ruamel.yaml import YAML
    from ruamel.yaml.comments import (
        CommentedBase,
        CommentedMap,
        CommentedOrderedMap,
        CommentedSeq,
        CommentedSet,
        Tag,
        TaggedScalar,
    )
except ModuleNotFoundError:
    from ruamel_yaml import YAML
    from ruamel_yaml.comments import (
        CommentedBase,
        CommentedMap,
        CommentedOrderedMap,
        CommentedSeq,
        CommentedSet,
        Tag,
        TaggedScalar,
    )
