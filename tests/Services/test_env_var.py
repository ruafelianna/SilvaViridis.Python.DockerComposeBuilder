import pytest

from itertools import product
from pydantic import ValidationError

from typing import Any

from SilvaViridis.Python.DockerComposeBuilder.Services import EnvVar

from ..fixtures import containers, empty, non_models

vars = ["var_x", "someVar"]

defaults = ["123", "abcde", "", None]

prod_var_default = list(product(vars, defaults))

## CREATION

@pytest.mark.parametrize("name,default_value", prod_var_default)
def test_create(name : str, default_value : str | None):
    env_var = EnvVar(name = name, default_value = default_value)
    assert (env_var.name, env_var.default_value) == (name, default_value)


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("name", empty)
@pytest.mark.parametrize("default_value", defaults)
def test_create_fail(name : str, default_value : str | None):
    EnvVar(name = name, default_value = default_value)

## API

@pytest.mark.parametrize("name,default_value", prod_var_default)
@pytest.mark.parametrize("container_name", containers)
def test_full_env_var(name : str, default_value : str | None, container_name : str):
    value = f"${{{container_name}__{name}}}" if default_value is None else default_value
    assert EnvVar(name = name, default_value = default_value).get_full_env_var(container_name) == {name: value}

## EQUALITY

@pytest.mark.parametrize("env_var1", prod_var_default)
@pytest.mark.parametrize("env_var2", prod_var_default)
def test_equal(env_var1 : tuple[str, str | None], env_var2 : tuple[str, str | None]):
    name1, default_value1 = env_var1
    name2, default_value2 = env_var2
    assert (EnvVar(name = name1, default_value = default_value1) == EnvVar(name = name2, default_value = default_value2)) == (name1 == name2)


@pytest.mark.parametrize("name,default_value", prod_var_default)
@pytest.mark.parametrize("other", non_models + vars)
def test_not_equal(name : str, default_value : str | None, other : Any):
    assert EnvVar(name = name, default_value = default_value) != other

## HASH

@pytest.mark.parametrize("name,default_value", prod_var_default)
def test_hash(name : str, default_value : str | None):
    assert hash(EnvVar(name = name, default_value = default_value)) == hash(name)

## REPR

@pytest.mark.parametrize("name,default_value", prod_var_default)
def test_repr(name : str, default_value : str | None):
    assert repr(EnvVar(name = name, default_value = default_value)) == f"{{'name': {repr(name)}, 'default_value': {repr(default_value)}}}"
