from __future__ import annotations

import pytest

from itertools import product

from SilvaViridis.Python.DockerComposeBuilder.Common import SELinuxRelabelingOption
from SilvaViridis.Python.DockerComposeBuilder.Models import VolumeBindOptions

from ..fixtures import (
    check_create_full,
    check_eq_full,
    check_full_volume_options,
    check_hash_full,
    check_repr_full,
    create_obj_from_dict,
    ternary_options,
)

LABELS = ["propagation", "create_host_path", "selinux"]

type TPrp = bool | None
type TChp = bool | None
type TSel = SELinuxRelabelingOption | None
type TAll = tuple[TPrp, TChp, TSel]

def create(args : TAll) -> VolumeBindOptions:
    return create_obj_from_dict(VolumeBindOptions, LABELS, *args)

propagation_values = ternary_options

create_host_path_values = ternary_options

selinux_values = list(SELinuxRelabelingOption) + [None]

valid_options = list(product(propagation_values, create_host_path_values, selinux_values))

propagation = True
create_host_path = False
selinux = SELinuxRelabelingOption.shared

full_options = [
    ((None, None, None), (None, None, None)),
    ((propagation, None, None), ("true", None, None)),
    ((None, create_host_path, None), (None, "false", None)),
    ((None, None, selinux), (None, None, "z")),
    ((propagation, create_host_path, selinux), ("true", "false", "z")),
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
