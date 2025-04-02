from __future__ import annotations

import pytest

from itertools import product
from typing import Any

from SilvaViridis.Python.DockerComposeBuilder.Common import SELinuxRelabelingOption
from SilvaViridis.Python.DockerComposeBuilder.Services import VolumeBindOptions

from ..fixtures import non_models

propagation_values : list[bool | None] = [True, False, None]

create_host_path_values : list[bool | None] = [True, False, None]

selinux_values : list[SELinuxRelabelingOption | None] = list(SELinuxRelabelingOption) + [None]

prod_propagation_create_host_path_selinux = list(product(propagation_values, create_host_path_values, selinux_values))

## CREATION

@pytest.mark.parametrize("propagation,create_host_path,selinux", prod_propagation_create_host_path_selinux)
def test_create(propagation : bool | None, create_host_path : bool | None, selinux : SELinuxRelabelingOption | None):
    options = VolumeBindOptions(propagation = propagation, create_host_path = create_host_path, selinux = selinux)
    assert (options.propagation, options.create_host_path, options.selinux) == (propagation, create_host_path, selinux)

## API

@pytest.mark.parametrize("propagation,create_host_path,selinux", prod_propagation_create_host_path_selinux)
def test_full_options(propagation : bool | None, create_host_path : bool | None, selinux : SELinuxRelabelingOption | None):
    options = VolumeBindOptions(propagation = propagation, create_host_path = create_host_path, selinux = selinux)
    expected : dict[str, str | None] = {
        "propagation": None if propagation is None else str(propagation).lower(),
        "create_host_path": None if create_host_path is None else str(create_host_path).lower(),
        "selinux": None if selinux is None else selinux.value,
    }
    expected = {k: v for k, v in expected.items() if v is not None}
    assert options.get_full_options() == expected

## EQUALITY

@pytest.mark.parametrize("propagation1,create_host_path1,selinux1", prod_propagation_create_host_path_selinux)
@pytest.mark.parametrize("propagation2,create_host_path2,selinux2", prod_propagation_create_host_path_selinux)
def test_equal(
    propagation1 : bool | None, create_host_path1 : bool | None, selinux1 : SELinuxRelabelingOption | None,
    propagation2 : bool | None, create_host_path2 : bool | None, selinux2 : SELinuxRelabelingOption | None,
):
    options1 = VolumeBindOptions(propagation = propagation1, create_host_path = create_host_path1, selinux = selinux1)
    options2 = VolumeBindOptions(propagation = propagation2, create_host_path = create_host_path2, selinux = selinux2)
    assert (options1 == options2) == (
        propagation1 == propagation2
        and create_host_path1 == create_host_path2
        and selinux1 == selinux2
    )


@pytest.mark.parametrize("propagation,create_host_path,selinux", prod_propagation_create_host_path_selinux)
@pytest.mark.parametrize("other", non_models)
def test_not_equal(propagation : bool | None, create_host_path : bool | None, selinux : SELinuxRelabelingOption | None, other : Any):
    options = VolumeBindOptions(propagation = propagation, create_host_path = create_host_path, selinux = selinux)
    assert options != other

## HASH

@pytest.mark.parametrize("propagation,create_host_path,selinux", prod_propagation_create_host_path_selinux)
def test_hash(propagation : bool | None, create_host_path : bool | None, selinux : SELinuxRelabelingOption | None):
    options = VolumeBindOptions(propagation = propagation, create_host_path = create_host_path, selinux = selinux)
    assert hash(options) == hash((propagation, create_host_path, selinux))

## REPR

@pytest.mark.parametrize("propagation,create_host_path,selinux", prod_propagation_create_host_path_selinux)
def test_repr(propagation : bool | None, create_host_path : bool | None, selinux : SELinuxRelabelingOption | None):
    options = VolumeBindOptions(propagation = propagation, create_host_path = create_host_path, selinux = selinux)
    assert repr(options) == f"{{'propagation': {repr(propagation)}, 'create_host_path': {repr(create_host_path)}, 'selinux': {repr(selinux)}}}"
