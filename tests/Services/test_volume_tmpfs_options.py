from __future__ import annotations

import pytest

from itertools import product

from SilvaViridis.Python.Common.Unix import PermissionLevel, UnixPermissions

from SilvaViridis.Python.DockerComposeBuilder.Services import VolumeTmpfsOptions

from ..fixtures import (
    check_create_full,
    check_eq_full,
    check_full_volume_options,
    check_hash_full,
    check_repr_full,
    create_obj_from_dict,
    create_unix_permission,
    unix_permissions,
)

LABELS = ["size", "mode"]

type TSze = int | None
type TMde = UnixPermissions | None
type TAll = tuple[TSze, TMde]

def create(args : TAll) -> VolumeTmpfsOptions:
    return create_obj_from_dict(VolumeTmpfsOptions, LABELS, *args)

size_values = [100, None]

mode_values = unix_permissions + [None]

valid_options = list(product(size_values, mode_values))

size = 12345
mode = create_unix_permission(PermissionLevel.r, PermissionLevel.w, PermissionLevel.x)

full_options = [
    ((None, None), (None, None)),
    ((size, None), ("12345", None)),
    ((None, mode), (None, "421")),
    ((size, mode), ("12345", "421")),
]

## CREATION

@pytest.mark.parametrize("options", valid_options)
def test_create(options : TAll):
    check_create_full(LABELS, options, create)

## API

@pytest.mark.parametrize("options,expected", full_options)
def test_full_options(options : TAll, expected : tuple[str | None, ...]):
    check_full_volume_options(options, LABELS, create, expected)

## EQUALITY

@pytest.mark.parametrize("options1", valid_options)
@pytest.mark.parametrize("options2", valid_options)
def test_equal(options1 : TAll, options2 : TAll):
    check_eq_full(options1, options2, create)

## HASH

@pytest.mark.parametrize("options", valid_options)
def test_hash(options : TAll):
    check_hash_full(options, create)

## REPR

@pytest.mark.parametrize("options", valid_options)
def test_repr(options : TAll):
    check_repr_full(LABELS, options, create)
