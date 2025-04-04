from __future__ import annotations

import pytest

from itertools import product

from SilvaViridis.Python.DockerComposeBuilder.Common import OS, Path
from SilvaViridis.Python.DockerComposeBuilder.Services import VolumeOptions

LABELS = ["nocopy", "subpath"]

type TNcp = bool | None
type TSbp = Path | None
type TAll = tuple[TNcp, TSbp]

nocopy_values : list[TNcp] = [True, False, None]

subpath_values : list[TSbp] = [
    Path(path = "/some/posix/path"),
    Path(path = "C:\\some\\nt\\path", os = OS.NT),
    None,
]

n0 = nocopy_values[0]
s0 : Path = subpath_values[0] # type: ignore

full_options = [
    ((None, None), (None, None)),
    ((n0, None), ("true", None)),
    ((None, s0), (None, s0.path)),
    ((n0, s0), ("true", s0.path)),
]

def create(nocopy : TNcp, subpath : TSbp):
    return VolumeOptions(nocopy = nocopy, subpath = subpath)

valid_options = list(product(nocopy_values, subpath_values))

## CREATION

@pytest.mark.parametrize("options", valid_options)
def test_create(options : TAll):
    options_obj = create(*options)
    assert (
        options_obj.nocopy,
        options_obj.subpath,
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
    nocopy1, subpath1 = options1
    nocopy2, subpath2 = options2
    assert (create(*options1) == create(*options2)) == (
        nocopy1 == nocopy2
        and subpath1 == subpath2
    )

## HASH

@pytest.mark.parametrize("options", valid_options)
def test_hash(options : TAll):
    assert hash(create(*options)) == hash(options)

## REPR

@pytest.mark.parametrize("options", valid_options)
def test_repr(options : TAll):
    nocopy, subpath = options
    assert repr(create(*options)) == f"{{'nocopy': {repr(nocopy)}, 'subpath': {repr(subpath)}}}"
