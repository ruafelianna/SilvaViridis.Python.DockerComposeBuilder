from __future__ import annotations

import pytest

from itertools import product

from SilvaViridis.Python.DockerComposeBuilder.Common import OS, Path
from SilvaViridis.Python.DockerComposeBuilder.Models import VolumeOptions

from ..fixtures import (
    check_create_full,
    check_eq_full,
    check_full_volume_options,
    check_hash_full,
    check_repr_full,
    create_obj_from_dict,
    ternary_options,
)

LABELS = ["nocopy", "subpath"]

type TNcp = bool | None
type TSbp = Path | None
type TAll = tuple[TNcp, TSbp]

def create(args : TAll) -> VolumeOptions:
    return create_obj_from_dict(VolumeOptions, LABELS, *args)

nocopy_values = ternary_options

subpath_values = [
    Path(path = "/some/posix/path"),
    Path(path = "C:\\some\\nt\\path", os = OS.NT),
    None,
]

valid_options = list(product(nocopy_values, subpath_values))

nocopy = True
subpath = Path(path = "/some/posix/path")

full_options = [
    ((None, None), (None, None)),
    ((nocopy, None), ("true", None)),
    ((None, subpath), (None, "/some/posix/path")),
    ((nocopy, subpath), ("true", "/some/posix/path")),
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
