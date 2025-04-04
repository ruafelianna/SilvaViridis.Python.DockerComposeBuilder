from __future__ import annotations

import pytest

from itertools import product

from SilvaViridis.Python.Common.Unix import PermissionLevel, UnixPermissions

from SilvaViridis.Python.DockerComposeBuilder.Services import VolumeTmpfsOptions

LABELS = ["size", "mode"]

type TSze = int | None
type TMde = UnixPermissions | None
type TAll = tuple[TSze, TMde]

size_values : list[TSze] = [100, None]

permissions = [
    (PermissionLevel.rw, PermissionLevel.none, PermissionLevel.wx),
    (PermissionLevel.x, PermissionLevel.r, PermissionLevel.rx),
    (PermissionLevel.r, PermissionLevel.rwx, PermissionLevel.none),
    (PermissionLevel.none, PermissionLevel.w, PermissionLevel.w),
    (PermissionLevel.wx, PermissionLevel.rwx, PermissionLevel.rwx),
]

mode_values : list[TMde] = [UnixPermissions(user = u, group = g, other = o) for u, g, o in permissions] + [None]

s0 = size_values[0]
u0 : UnixPermissions = mode_values[0] # type: ignore

full_options = [
    ((None, None), (None, None)),
    ((s0, None), ("100", None)),
    ((None, u0), (None, u0.as_octal())),
    ((s0, u0), ("100", u0.as_octal())),
]

def create(size : TSze, mode : TMde):
    return VolumeTmpfsOptions(size = size, mode = mode)

valid_options = list(product(size_values, mode_values))

## CREATION

@pytest.mark.parametrize("options", valid_options)
def test_create(options : TAll):
    options_obj = create(*options)
    assert (
        options_obj.size,
        options_obj.mode,
    ) == options

## API

@pytest.mark.parametrize("options,expected", full_options)
def test_full_options(options : TAll, expected : tuple[str | None, str | None]):
    result = {l: e for l, e in map(lambda l, e: (l, e), LABELS, expected) if e is not None} 
    assert create(*options).get_full_options() == result

## EQUALITY

@pytest.mark.parametrize("options1", valid_options)
@pytest.mark.parametrize("options2", valid_options)
def test_equal(options1 : TAll, options2 : TAll):
    size1, mode1 = options1
    size2, mode2 = options2
    assert (create(*options1) == create(*options2)) == (
        size1 == size2
        and mode1 == mode2
    )

## HASH

@pytest.mark.parametrize("options", valid_options)
def test_hash(options : TAll):
    assert hash(create(*options)) == hash(options)

## REPR

@pytest.mark.parametrize("options", valid_options)
def test_repr(options : TAll):
    size, mode = options
    assert repr(create(*options)) == f"{{'size': {repr(size)}, 'mode': {repr(mode)}}}"
