import pytest

from itertools import product
from pydantic import ValidationError

from SilvaViridis.Python.DockerComposeBuilder.Common import Configuration
from SilvaViridis.Python.DockerComposeBuilder.Models import EnvVar

from ..fixtures import (
    check_create_full,
    check_repr_full,
    create_obj_from_dict,
    empty,
)

LABELS = ["name", "default_value"]

type TVar = str
type TDef = str | None
type TAll = tuple[TVar, TDef]

def create(args : TAll) -> EnvVar:
    return create_obj_from_dict(EnvVar, LABELS, *args)

name_values = ["var_x", "someVar"]

default_values = ["123", "", None]

valid_vars = list(product(name_values, default_values))

invalid_vars = list(product(empty, default_values))

name = "var_x"
default_1 = "123"
default_2 = ""
container_name = "apple"

full_env_vars = [
    ((name, None), container_name, "${apple__var_x}"),
    ((name, default_1), container_name, "123"),
    ((name, default_2), container_name, ""),
]

## CREATION

@pytest.mark.parametrize("env_var", valid_vars)
def test_create(env_var : TAll):
    check_create_full(LABELS, env_var, create)


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("env_var", invalid_vars)
def test_create_fail(env_var : TAll):
    create(env_var)

## API

@pytest.mark.parametrize("env_var,container_name,expected", full_env_vars)
def test_full_env_var(env_var : TAll, container_name : str, expected : Configuration):
    name, _ = env_var
    assert create(env_var).get_full_env_var(container_name) == {name: expected}

## EQUALITY

@pytest.mark.parametrize("env_var1", valid_vars)
@pytest.mark.parametrize("env_var2", valid_vars)
def test_equal(env_var1 : TAll, env_var2 : TAll):
    name1, _ = env_var1
    name2, _ = env_var2
    assert (create(env_var1) == create(env_var2)) == (name1 == name2)

## HASH

@pytest.mark.parametrize("env_var", valid_vars)
def test_hash(env_var : TAll):
    name, _ = env_var
    assert hash(create(env_var)) == hash(name)

## REPR

@pytest.mark.parametrize("env_var", valid_vars)
def test_repr(env_var : TAll):
    check_repr_full(LABELS, env_var, create)
