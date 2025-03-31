from __future__ import annotations

import pytest

from itertools import product
from typing import Any

from SilvaViridis.Python.Common.Unix import Permission, UnixPermission, UnixPermissionTypeHint

from SilvaViridis.Python.DockerComposeBuilder.Services import VolumeTmpfsOptions

from ..fixtures import non_models

size_values : list[int | None] = [100, None]

permissions = [
    (Permission.rw, Permission.none, Permission.wx),
    (Permission.x, Permission.r, Permission.rx),
    (Permission.r, Permission.rwx, Permission.none),
    (Permission.none, Permission.w, Permission.w),
    (Permission.wx, Permission.rwx, Permission.rwx),
]

mode_values : list[UnixPermissionTypeHint | None] = [UnixPermission(u, g, o) for u, g, o in permissions] + [None]

prod_size_mode = list(product(size_values, mode_values))

## CREATION

@pytest.mark.parametrize("size,mode", prod_size_mode)
def test_create(size : int | None, mode : UnixPermissionTypeHint | None):
    options = VolumeTmpfsOptions(size, mode)
    assert (options.size, options.mode) == (size, mode)

## API

@pytest.mark.parametrize("size,mode", prod_size_mode)
def test_full_options(size : int | None, mode : UnixPermissionTypeHint | None):
    options = VolumeTmpfsOptions(size, mode)
    expected : dict[str, str | None] = {
        "size": None if size is None else str(size),
        "mode": None if mode is None else mode.as_octal(),
    }
    expected = {k: v for k, v in expected.items() if v is not None}
    assert options.get_full_options() == expected

## EQUALITY

@pytest.mark.parametrize("size1,mode1", prod_size_mode)
@pytest.mark.parametrize("size2,mode2", prod_size_mode)
def test_equal(size1 : int | None, mode1 : UnixPermissionTypeHint | None, size2 : bool | None, mode2 : UnixPermissionTypeHint | None):
    options1 = VolumeTmpfsOptions(size1, mode1)
    options2 = VolumeTmpfsOptions(size2, mode2)
    assert (options1 == options2) == (size1 == size2 and mode1 == mode2)


@pytest.mark.parametrize("size,mode", prod_size_mode)
@pytest.mark.parametrize("other", non_models)
def test_not_equal(size : int | None, mode : UnixPermissionTypeHint | None, other : Any):
    options = VolumeTmpfsOptions(size, mode)
    assert options != other

## HASH

@pytest.mark.parametrize("size,mode", prod_size_mode)
def test_hash(size : int | None, mode : UnixPermissionTypeHint | None):
    options = VolumeTmpfsOptions(size, mode)
    assert hash(options) == hash((size, mode))

## REPR

@pytest.mark.parametrize("size,mode", prod_size_mode)
def test_repr(size : int | None, mode : UnixPermissionTypeHint | None):
    options = VolumeTmpfsOptions(size, mode)
    assert repr(options) == f"{{'size': {repr(size)}, 'mode': {repr(mode)}}}"
