import pytest

from pydantic import ValidationError
from typing import Any

from SilvaViridis.Python.DockerComposeBuilder.Common import OS, Path

from ..fixtures import empty, non_models

nt_paths = ["C:\\some\\nt\\path"]

posix_paths = ["/some/posix/path"]

map_nt_paths = [(p, OS.NT) for p in nt_paths]

map_posix_paths = [(p, OS.POSIX) for p in posix_paths]

all_paths = map_nt_paths + map_posix_paths

all_paths_str = [p[0] for p in all_paths]

nt_path_parts : list[str | Path] = ["C:\\", "some", "nt", "path"]

posix_path_parts : list[str | Path] = ["/", "some", "posix", "path"]

## CREATION

@pytest.mark.parametrize("path,os", all_paths)
def test_create(path : str, os : OS):
    path_obj = Path(path = path, os = os)
    assert (path_obj.path, path_obj.os) == (path, os)


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("path", empty)
@pytest.mark.parametrize("os", OS)
def test_create_fail(path : str, os : OS):
    Path(path = path, os = os)

## API

@pytest.mark.parametrize("parts,os_parts,path,os_path", [
    (nt_path_parts, OS.NT, nt_paths[0], OS.NT),
    (posix_path_parts, OS.POSIX, posix_paths[0], OS.POSIX),
])
def test_join(parts : list[str | Path], os_parts : OS, path : str, os_path : OS):
    parts[3] = Path(path = str(parts[3]), os = os_path)
    assert Path.join(os_parts, parts) == path


@pytest.mark.xfail(raises = ValueError)
@pytest.mark.parametrize("parts,os_parts,os_path", [
    (nt_path_parts, OS.NT, OS.POSIX),
    (posix_path_parts, OS.POSIX, OS.NT),
])
def test_join_value_fail(parts : list[str | Path], os_parts : OS, os_path : OS):
    parts[3] = Path(path = str(parts[3]), os = os_path)
    Path.join(os_parts, parts)


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("parts,os_parts", [
    ([], OS.POSIX),
    ([""], OS.POSIX),
    ([" "], OS.POSIX),
    (["\t"], OS.NT),
    (["\n"], OS.NT),
    ([None], OS.NT),
])
def test_join_validation_fail(parts : list[str | Path], os_parts : OS):
    Path.join(os_parts, parts)

## STR

@pytest.mark.parametrize("path,os", all_paths)
def test_str(path : str, os : OS):
    assert str(Path(path = path, os = os)) == path

## EQUALITY

@pytest.mark.parametrize("path1,os1", all_paths)
@pytest.mark.parametrize("path2,os2", all_paths)
def test_equal(path1 : str, os1 : OS, path2 : str, os2 : OS):
    assert (Path(path = path1, os = os1) == Path(path = path2, os = os2)) == (path1 == path2)


@pytest.mark.parametrize("path,os", all_paths)
@pytest.mark.parametrize("other", non_models + all_paths_str)
def test_not_equal(path : str, os : OS, other : Any):
    assert Path(path = path, os = os) != other

## HASH

@pytest.mark.parametrize("path,os", all_paths)
def test_hash(path : str, os : OS):
    assert hash(Path(path = path, os = os)) == hash(path)

## REPR

@pytest.mark.parametrize("path,os", all_paths)
def test_repr(path : str, os : OS):
    assert repr(Path(path = path, os = os)) == f"{{'path': {repr(path)}, 'os': {repr(os)}}}"
