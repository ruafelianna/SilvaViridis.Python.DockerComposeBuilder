from collections.abc import Callable, Mapping
from typing import Any

class Node:
    ...

class ScalarNode(Node):
    ...

class Dumper:
    def represent_scalar(self, tag : str, value : Any, style : str | None = None) -> ScalarNode: ...

def add_representer[T](data_type : type, representer : Callable[[Dumper, T], Node]) -> None: ...

def dump(
    data : Any,
    stream : None = None,
    Dumper : ... = ...,
    *,
    default_style: str | None = None,
    default_flow_style: bool | None = False,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | None = None,
    allow_unicode: bool | None = None,
    line_break: str | None = None,
    encoding: None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: tuple[int, int] | None = None,
    tags: Mapping[str, str] | None = None,
    sort_keys: bool = True) -> str: ...
