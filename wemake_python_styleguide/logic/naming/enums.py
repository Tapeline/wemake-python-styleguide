import ast
from collections.abc import Collection
from typing import Final

from wemake_python_styleguide.logic.source import node_to_string

_ENUM_NAMES: Final = (
    'enum.Enum',
    'enum.EnumType',
    'enum.EnumMeta',
    'Enum',
    'EnumType',
    'EnumMeta',
)

_ENUM_LIKE_NAMES: Final = (
    *_ENUM_NAMES,
    'Choices',
    'models.Choices',
    'IntegerChoices',
    'models.IntegerChoices',
    'TextChoices',
    'models.TextChoices',
)


def _has_one_of_base_classes(
    defn: ast.ClassDef, base_names: Collection[str]
) -> bool:
    """Tells whether some class has one of provided names as its base."""
    string_bases = {node_to_string(base) for base in defn.bases}
    return any(enum_base in string_bases for enum_base in base_names)


def has_enum_base(defn: ast.ClassDef) -> bool:
    """Tells whether some class has `Enum` or similar class as its base."""
    return _has_one_of_base_classes(defn, _ENUM_NAMES)


def has_enum_like_base(defn: ast.ClassDef) -> bool:
    """
    Tells whether some class has `Enum` or semantically similar class as its base.
    Unlike has_enum_base it also includes support for Django Choices
    """
    return _has_one_of_base_classes(defn, _ENUM_LIKE_NAMES)
