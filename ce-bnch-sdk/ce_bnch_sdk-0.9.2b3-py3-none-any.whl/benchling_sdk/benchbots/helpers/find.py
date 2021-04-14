from typing import Any, Callable, List, Optional, TypeVar

T = TypeVar("T")


def find(objs: List[T], fn: Callable[[T], bool]) -> Optional[T]:
    matches = [obj for obj in objs if fn(obj)]
    assert len(matches) <= 1
    return matches[0] if matches else None


def find_by_id_or_name(objs: List[Any], id_or_name: str) -> Optional[Any]:
    return find(objs, lambda o: o.id == id_or_name or o.name == id_or_name)
