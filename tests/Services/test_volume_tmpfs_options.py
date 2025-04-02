from __future__ import annotations

import pytest

from itertools import product
from typing import Any

from SilvaViridis.Python.Common.Unix import PermissionLevel, UnixPermissions

from SilvaViridis.Python.DockerComposeBuilder.Services import VolumeTmpfsOptions

from ..fixtures import non_models

size_values : list[int | None] = [100, None]

permissions = [
    (PermissionLevel.rw, PermissionLevel.none, PermissionLevel.wx),
    (PermissionLevel.x, PermissionLevel.r, PermissionLevel.rx),
    (PermissionLevel.r, PermissionLevel.rwx, PermissionLevel.none),
    (PermissionLevel.none, PermissionLevel.w, PermissionLevel.w),
    (PermissionLevel.wx, PermissionLevel.rwx, PermissionLevel.rwx),
]

mode_values : list[UnixPermissions | None] = [UnixPermissions(user = u, group = g, other = o) for u, g, o in permissions] + [None]

prod_size_mode = list(product(size_values, mode_values))

## CREATION

@pytest.mark.parametrize("size,mode", prod_size_mode)
def test_create(size : int | None, mode : UnixPermissions | None):
    options = VolumeTmpfsOptions(size = size, mode = mode)
    assert (options.size, options.mode) == (size, mode)

## API

@pytest.mark.parametrize("size,mode", prod_size_mode)
def test_full_options(size : int | None, mode : UnixPermissions | None):
    options = VolumeTmpfsOptions(size = size, mode = mode)
    expected : dict[str, str | None] = {
        "size": None if size is None else str(size),
        "mode": None if mode is None else mode.as_octal(),
    }
    expected = {k: v for k, v in expected.items() if v is not None}
    assert options.get_full_options() == expected

## EQUALITY

@pytest.mark.parametrize("size1,mode1", prod_size_mode)
@pytest.mark.parametrize("size2,mode2", prod_size_mode)
def test_equal(size1 : int | None, mode1 : UnixPermissions | None, size2 : bool | None, mode2 : UnixPermissions | None):
    options1 = VolumeTmpfsOptions(size = size1, mode = mode1)
    options2 = VolumeTmpfsOptions(size = size2, mode = mode2)
    assert (options1 == options2) == (size1 == size2 and mode1 == mode2)


@pytest.mark.parametrize("size,mode", prod_size_mode)
@pytest.mark.parametrize("other", non_models)
def test_not_equal(size : int | None, mode : UnixPermissions | None, other : Any):
    options = VolumeTmpfsOptions(size = size, mode = mode)
    assert options != other

## HASH

@pytest.mark.parametrize("size,mode", prod_size_mode)
def test_hash(size : int | None, mode : UnixPermissions | None):
    options = VolumeTmpfsOptions(size = size, mode = mode)
    assert hash(options) == hash((size, mode))

## REPR

@pytest.mark.parametrize("size,mode", prod_size_mode)
def test_repr(size : int | None, mode : UnixPermissions | None):
    options = VolumeTmpfsOptions(size = size, mode = mode)
    assert repr(options) == f"{{'size': {repr(size)}, 'mode': {repr(mode)}}}"
