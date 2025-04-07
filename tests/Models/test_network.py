from __future__ import annotations

import pytest

from itertools import product

from SilvaViridis.Python.DockerComposeBuilder.Common import Configuration
from SilvaViridis.Python.DockerComposeBuilder.Models import Network

from ..fixtures import (
    check_create_full,
    check_eq_full,
    check_repr_full,
    create_obj_from_dict,
)

LABELS = ["name"]

type TNme = str
type TAll = tuple[TNme]

def create(args : TAll) -> Network:
    return create_obj_from_dict(Network, LABELS, *args)

name_values = ["banana"]

valid_networks = list(product(name_values))

full_networks = [
    (("banana",), "banana"),
]

## CREATION

@pytest.mark.parametrize("network", valid_networks)
def test_create(network : TAll):
    check_create_full(LABELS, network, create)

## API

@pytest.mark.parametrize("network,expected", full_networks)
def test_full_network(network : TAll, expected : Configuration):
    assert create(network).get_full_network() == expected

## EQUALITY

@pytest.mark.parametrize("network1", valid_networks)
@pytest.mark.parametrize("network2", valid_networks)
def test_equal(network1 : TAll, network2 : TAll):
    check_eq_full(network1, network2, create)

## HASH

@pytest.mark.parametrize("network", valid_networks)
def test_hash(network : TAll):
    name, = network
    assert hash(create(network)) == hash(name)

## REPR

@pytest.mark.parametrize("network", valid_networks)
def test_repr(network : TAll):
    check_repr_full(LABELS, network, create)
