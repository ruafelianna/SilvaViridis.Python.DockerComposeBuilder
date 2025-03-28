import pytest

from beartype.roar import BeartypeCallHintViolation
from itertools import product
from typing import Any

from SilvaViridis.Python.DockerComposeBuilder.Models import EnvVar

from ..fixtures import containers, empty, non_models

vars = ["var_x", "someVar"]

defaults = ["123", "abcde", "", None]

prod_var_default = list(product(vars, defaults))

prod_all = list(product(prod_var_default, repeat = 2))

full_vars = [(n, d, n) for n, d in prod_var_default]

prod_empty_default = list(product(empty, defaults))

map_hashes = [(n, d, hash(n)) for n, d in prod_var_default]

map_repr = [(n, d, f"{{'name': {repr(n)}, 'default_value': {repr(d)}}}") for n, d in prod_var_default]

## CREATION

@pytest.mark.parametrize("name,default_value", prod_var_default)
def test_create(name : str, default_value : str | None):
    env_var = EnvVar(name, default_value)
    assert (env_var.name, env_var.default_value) == (name, default_value)


@pytest.mark.xfail(raises = BeartypeCallHintViolation)
@pytest.mark.parametrize("name,default_value", prod_empty_default)
def test_create_fail(name : str, default_value : str | None):
    EnvVar(name, default_value)

## API

@pytest.mark.parametrize("name,default_value", prod_var_default)
@pytest.mark.parametrize("container_name", containers)
def test_full_env_var(name : str, default_value : str | None, container_name : str):
    value = f"${{{container_name}__{name}}}" if default_value is None else default_value
    assert EnvVar(name, default_value).get_full_env_var(container_name) == {name: value}

## EQUALITY

@pytest.mark.parametrize("env_var1,env_var2", prod_all)
def test_equal(env_var1 : tuple[str, str | None], env_var2 : tuple[str, str | None]):
    name1, default_value1 = env_var1
    name2, default_value2 = env_var2
    assert (EnvVar(name1, default_value1) == EnvVar(name2, default_value2)) == (name1 == name2)


@pytest.mark.parametrize("name,default_value", prod_var_default)
@pytest.mark.parametrize("other", non_models + vars)
def test_not_equal(name : str, default_value : str | None, other : Any):
    assert EnvVar(name, default_value) != other

## HASH

@pytest.mark.parametrize("name,default_value,expected", map_hashes)
def test_hash(name : str, default_value : str | None, expected : int):
    assert hash(EnvVar(name, default_value)) == expected

## REPR

@pytest.mark.parametrize("name,default_value,expected", map_repr)
def test_repr(name : str, default_value : str | None, expected : str):
    assert repr(EnvVar(name, default_value)) == expected
