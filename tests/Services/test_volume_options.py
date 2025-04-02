from __future__ import annotations

import pytest

from itertools import product
from typing import Any

from SilvaViridis.Python.DockerComposeBuilder.Common import OS, Path
from SilvaViridis.Python.DockerComposeBuilder.Services import VolumeOptions

from ..fixtures import non_models

nocopy_values : list[bool | None] = [True, False, None]

subpath_values : list[Path | None] = [
    Path(path = "/some/posix/path"),
    Path(path = "C:\\some\\nt\\path", os = OS.NT),
    None,
]

prod_nocopy_subpath = list(product(nocopy_values, subpath_values))

## CREATION

@pytest.mark.parametrize("nocopy,subpath", prod_nocopy_subpath)
def test_create(nocopy : bool | None, subpath : Path | None):
    options = VolumeOptions(nocopy, subpath)
    assert (options.nocopy, options.subpath) == (nocopy, subpath)

## API

@pytest.mark.parametrize("nocopy,subpath", prod_nocopy_subpath)
def test_full_options(nocopy : bool | None, subpath : Path | None):
    options = VolumeOptions(nocopy, subpath)
    expected : dict[str, str | None] = {
        "nocopy": None if nocopy is None else str(nocopy).lower(),
        "subpath": None if subpath is None else subpath.path,
    }
    expected = {k: v for k, v in expected.items() if v is not None}
    assert options.get_full_options() == expected

## EQUALITY

@pytest.mark.parametrize("nocopy1,subpath1", prod_nocopy_subpath)
@pytest.mark.parametrize("nocopy2,subpath2", prod_nocopy_subpath)
def test_equal(nocopy1 : bool | None, subpath1 : Path | None, nocopy2 : bool | None, subpath2 : Path | None):
    options1 = VolumeOptions(nocopy1, subpath1)
    options2 = VolumeOptions(nocopy2, subpath2)
    assert (options1 == options2) == (nocopy1 == nocopy2 and subpath1 == subpath2)


@pytest.mark.parametrize("nocopy,subpath", prod_nocopy_subpath)
@pytest.mark.parametrize("other", non_models)
def test_not_equal(nocopy : bool | None, subpath : Path | None, other : Any):
    options = VolumeOptions(nocopy, subpath)
    assert options != other

## HASH

@pytest.mark.parametrize("nocopy,subpath", prod_nocopy_subpath)
def test_hash(nocopy : bool | None, subpath : Path | None):
    options = VolumeOptions(nocopy, subpath)
    assert hash(options) == hash((nocopy, subpath))

## REPR

@pytest.mark.parametrize("nocopy,subpath", prod_nocopy_subpath)
def test_repr(nocopy : bool | None, subpath : Path | None):
    options = VolumeOptions(nocopy, subpath)
    assert repr(options) == f"{{'nocopy': {repr(nocopy)}, 'subpath': {repr(subpath)}}}"
