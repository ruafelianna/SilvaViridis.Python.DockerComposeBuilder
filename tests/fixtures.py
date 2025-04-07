from collections.abc import Callable, Sequence
from os import getenv
from typing import Any

from SilvaViridis.Python.Common.Unix import PermissionLevel, UnixPermissions

from SilvaViridis.Python.DockerComposeBuilder.Services import IVolumeOptions

DCG_BASE_DATA_FOLDER = getenv("DCG_BASE_DATA_FOLDER")

empty : list[str | None] = ["", "\n", "\t", " ", None]

containers = ["apple"]

binary_options = [False, True]

ternary_options = binary_options + [None]

permissions = [
    (PermissionLevel.rw, PermissionLevel.none, PermissionLevel.wx),
    (PermissionLevel.x, PermissionLevel.r, PermissionLevel.rx),
    (PermissionLevel.r, PermissionLevel.rwx, PermissionLevel.none),
    (PermissionLevel.none, PermissionLevel.w, PermissionLevel.w),
    (PermissionLevel.wx, PermissionLevel.rwx, PermissionLevel.rwx),
]

def create_unix_permission(user : PermissionLevel, group : PermissionLevel, other : PermissionLevel):
    return UnixPermissions(user = user, group = group, other = other)

unix_permissions = [create_unix_permission(u, g, o) for u, g, o in permissions]


def create_obj_from_dict[TObj](
    obj : type[TObj],
    labels : Sequence[str],
    *args : Any,
) -> TObj:
    kwargs = dict(map(lambda l, a : (l, a), labels, args))
    return obj(**kwargs)


def check_create_full[TAll : tuple[Any, ...], TObj](
    labels : Sequence[str],
    args : TAll,
    create : Callable[[TAll], TObj],
) -> None:
    obj = create(args)
    assert tuple([getattr(obj, l) for l in labels]) == args


def check_eq_full[TAll : tuple[Any, ...], TObj](
    args1 : TAll,
    args2 : TAll,
    create : Callable[[TAll], TObj],
) -> None:
    assert (create(args1) == create(args2)) == all(list(map(lambda e1, e2: e1 == e2, args1, args2)))


def check_hash_full[TAll : tuple[Any, ...], TObj](
    args : TAll,
    create : Callable[[TAll], TObj],
) -> None:
    assert hash(create(args)) == hash(args)


def check_repr_full[TAll : tuple[Any, ...], TObj](
    labels : Sequence[str],
    args : TAll,
    create : Callable[[TAll], TObj],
) -> None:
    result = list(map(lambda l, a: f"'{l}': {repr(a)}", labels, args))
    assert repr(create(args)) == f"{{{", ".join(result)}}}"


def check_full_volume_options[TAll : tuple[Any, ...]](
    options : TAll,
    labels : Sequence[str],
    create : Callable[[TAll], IVolumeOptions],
    expected : Sequence[str | None],
) -> None:
    result = {l: e for l, e in map(lambda l, e: (l, e), labels, expected) if e is not None} 
    assert create(options).get_full_options() == result
