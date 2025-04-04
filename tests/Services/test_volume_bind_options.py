from __future__ import annotations

import pytest

from itertools import product

from SilvaViridis.Python.DockerComposeBuilder.Common import SELinuxRelabelingOption
from SilvaViridis.Python.DockerComposeBuilder.Services import VolumeBindOptions

type TPrp = bool | None
type TChp = bool | None
type TSel = SELinuxRelabelingOption | None
type TAll = tuple[TPrp, TChp, TSel]

LABELS = ["propagation", "create_host_path", "selinux"]

propagation_values : list[TPrp] = [True, False, None]

create_host_path_values : list[TChp] = [True, False, None]

selinux_values : list[TSel] = list(SELinuxRelabelingOption) + [None]

p0 = propagation_values[0]
c1 = create_host_path_values[1]
s0 : SELinuxRelabelingOption = selinux_values[0] # type: ignore

full_options = [
    ((p0, None, None), ("true", None, None)),
    ((None, c1, None), (None, "false", None)),
    ((None, None, s0), (None, None, s0.value)),
    ((p0, c1, s0), ("true", "false", s0.value)),
]

def create(propagation : TPrp, create_host_path : TChp, selinux : TSel):
    return VolumeBindOptions(propagation = propagation, create_host_path = create_host_path, selinux = selinux)

valid_options = list(product(propagation_values, create_host_path_values, selinux_values))

## CREATION

@pytest.mark.parametrize("options", valid_options)
def test_create(options : TAll):
    options_obj = create(*options)
    assert (
        options_obj.propagation,
        options_obj.create_host_path,
        options_obj.selinux
    ) == options

## API

@pytest.mark.parametrize("options,expected", full_options)
def test_full_options(options : TAll, expected : tuple[str | None, str | None, str | None]):
    result = {l: e for l, e in map(lambda l, e: (l, e), LABELS, expected) if e is not None}
    assert create(*options).get_full_options() == result

## EQUALITY

@pytest.mark.parametrize("options1", valid_options)
@pytest.mark.parametrize("options2", valid_options)
def test_equal(options1 : TAll, options2 : TAll):
    propagation1, create_host_path1, selinux1 = options1
    propagation2, create_host_path2, selinux2 = options2
    assert (create(*options1) == create(*options2)) == (
        propagation1 == propagation2
        and create_host_path1 == create_host_path2
        and selinux1 == selinux2
    )

## HASH

@pytest.mark.parametrize("options", valid_options)
def test_hash(options : TAll):
    assert hash(create(*options)) == hash(options)

## REPR

@pytest.mark.parametrize("options", valid_options)
def test_repr(options : TAll):
    propagation, create_host_path, selinux = options
    assert repr(create(*options)) == f"{{'propagation': {repr(propagation)}, 'create_host_path': {repr(create_host_path)}, 'selinux': {repr(selinux)}}}"
