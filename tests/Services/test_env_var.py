import pytest

from itertools import product
from pydantic import ValidationError

from SilvaViridis.Python.DockerComposeBuilder.Services import EnvVar

from ..fixtures import containers, empty

type TVar = str
type TDef = str | None
type TAll = tuple[TVar, TDef]

vars = ["var_x", "someVar"]

defaults = ["123", "", None]

v0 = vars[0]
d0 = defaults[0]
d1 = defaults[1]
c0 = containers[0]

full_env_vars = [
    ((v0, None), c0, f"${{{c0}__{v0}}}"),
    ((v0, d0), c0, d0),
    ((v0, d1), c0, ""),
]

def create(name : TVar, default_value : TDef):
    return EnvVar(
        name = name,
        default_value = default_value,
    )

valid_vars = list(product(vars, defaults))

invalid_vars = list(product(empty, defaults))

## CREATION

@pytest.mark.parametrize("env_var", valid_vars)
def test_create(env_var : TAll):
    env_var_obj = create(*env_var)
    assert (
        env_var_obj.name,
        env_var_obj.default_value,
    ) == env_var


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("env_var", invalid_vars)
def test_create_fail(env_var : TAll):
    create(*env_var)

## API

@pytest.mark.parametrize("env_var,container_name,expected", full_env_vars)
def test_full_env_var(env_var : TAll, container_name : str, expected : str):
    name, _ = env_var
    assert create(*env_var).get_full_env_var(container_name) == {name: expected}

## EQUALITY

@pytest.mark.parametrize("env_var1", valid_vars)
@pytest.mark.parametrize("env_var2", valid_vars)
def test_equal(env_var1 : TAll, env_var2 : TAll):
    name1, _ = env_var1
    name2, _ = env_var2
    assert (create(*env_var1) == create(*env_var2)) == (name1 == name2)

## HASH

@pytest.mark.parametrize("env_var", valid_vars)
def test_hash(env_var : TAll):
    name, _ = env_var
    assert hash(create(*env_var)) == hash(name)

## REPR

@pytest.mark.parametrize("env_var", valid_vars)
def test_repr(env_var : TAll):
    name, default_value = env_var
    assert repr(create(*env_var)) == f"{{'name': {repr(name)}, 'default_value': {repr(default_value)}}}"
