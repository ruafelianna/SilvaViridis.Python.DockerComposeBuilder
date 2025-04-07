import pytest

from itertools import product
from pydantic import ValidationError
from random import choice

from SilvaViridis.Python.DockerComposeBuilder.Common import OS, Path

from ..fixtures import (
    check_create_full,
    check_repr_full,
    create_obj_from_dict,
    empty,
)

LABELS = ["path", "os"]

type TPth = str
type TOs_ = OS | None
type TAll = tuple[TPth, TOs_]

def create(args : TAll) -> Path:
    return create_obj_from_dict(Path, LABELS, *args)

def valid(args : TAll) -> bool:
    path, os = args

    return (
        path == path_values[0] and os == OS.NT
        or path == path_values[1] and os == OS.POSIX
    )

path_values = ["C:\\some\\nt\\path", "/some/posix/path"]

os_values = list(OS)

prod_all = list(product(path_values, os_values))

valid_paths = [t for t in prod_all if valid(t)]

parts_1 : list[str | Path] = ["C:\\", "some", "nt", "path"]
parts_2 : list[str | Path] = ["/", "some", "posix", "path"]
os_1 = OS.NT
os_2 = OS.POSIX

join_paths = [
    (parts_1, os_1, "C:\\some\\nt\\path"),
    (parts_2, os_2, "/some/posix/path"),
]

join_paths_fail = [[e] for e in empty] \
    + [[], [create(('a', OS.NT)), create(('b', OS.POSIX))]]

## CREATION

@pytest.mark.parametrize("path", valid_paths)
def test_create(path : TAll):
    check_create_full(LABELS, path, create)

## API

@pytest.mark.parametrize("parts,os,expected", join_paths)
def test_join(parts : list[str | Path], os : OS, expected : str):
    assert Path.join(os, parts) == expected


@pytest.mark.xfail(raises = (ValidationError, ValueError))
@pytest.mark.parametrize("parts", join_paths_fail)
def test_join_validation_fail(parts : list[str | Path]):
    Path.join(choice(os_values), parts)

## STR

@pytest.mark.parametrize("path", valid_paths)
def test_str(path : TAll):
    p, _ = path
    assert str(create(path)) == p

## EQUALITY

@pytest.mark.parametrize("path1", valid_paths)
@pytest.mark.parametrize("path2", valid_paths)
def test_equal(path1 : TAll, path2 : TAll):
    p1, _ = path1
    p2, _ = path2
    assert (create(path1) == create(path2)) == (p1 == p2)

## HASH

@pytest.mark.parametrize("path", valid_paths)
def test_hash(path : TAll):
    p, _ = path
    assert hash(create(path)) == hash(p)

## REPR

@pytest.mark.parametrize("path", valid_paths)
def test_repr(path : TAll):
    check_repr_full(LABELS, path, create)
