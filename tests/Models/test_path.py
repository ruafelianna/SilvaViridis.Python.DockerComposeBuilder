import pytest

from beartype.roar import BeartypeCallHintViolation
from typing import Any

from SilvaViridis.Python.DockerComposeBuilder.Enums import OS
from SilvaViridis.Python.DockerComposeBuilder.Models import Path

from ..fixtures import empty, non_models

nt_paths = ["C:\\some\\nt\\path", "C:\\some\\nt\\path 2"]

posix_paths = ["/some/posix/path", "/some/posix/path 2"]

map_nt_paths = [(p, OS.NT) for p in nt_paths]

map_posix_paths = [(p, OS.POSIX) for p in posix_paths]

all_paths = map_nt_paths + map_posix_paths

all_paths_str = [p[0] for p in all_paths]

map_hashes = [(p, o, hash(p)) for p, o in all_paths]

map_repr = [(p, o, f"{{'path': {repr(p)}, 'os': {repr(o)}}}") for p, o in all_paths]

nt_parts : list[str | Path] = ["C:\\", "some", "nt", "path"]

posix_parts : list[str | Path] = ["/", "some", "posix", "path"]

## CREATION

@pytest.mark.parametrize("path,os", all_paths)
def test_create(path : str, os : OS):
    path_obj = Path(path, os)
    assert (path_obj.path, path_obj.os) == (path, os)


@pytest.mark.xfail(raises = BeartypeCallHintViolation)
@pytest.mark.parametrize("path", empty)
@pytest.mark.parametrize("os", OS)
def test_create_fail(path : str, os : OS):
    Path(path, os)

## API

@pytest.mark.parametrize("parts,os_parts,path,os_path", [
    (nt_parts, OS.NT, nt_paths[0], OS.NT),
    (posix_parts, OS.POSIX, posix_paths[0], OS.POSIX),
])
def test_join(parts : list[str | Path], os_parts : OS, path : str, os_path : OS):
    parts[3] = Path(str(parts[3]), os_path)
    assert Path.join(os_parts, *parts) == path


@pytest.mark.xfail(raises = ValueError)
@pytest.mark.parametrize("parts,os_parts,os_path", [
    (nt_parts, OS.NT, OS.POSIX),
    (posix_parts, OS.POSIX, OS.NT),
])
def test_join_fail(parts : list[str | Path], os_parts : OS, os_path : OS):
    parts[3] = Path(str(parts[3]), os_path)
    Path.join(os_parts, *parts)

## STR

@pytest.mark.parametrize("path,os", all_paths)
def test_str(path : str, os : OS):
    assert str(Path(path, os)) == path

## EQUALITY

@pytest.mark.parametrize("path1,os1", all_paths)
@pytest.mark.parametrize("path2,os2", all_paths)
def test_equal(path1 : str, os1 : OS, path2 : str, os2 : OS):
    assert (Path(path1, os1) == Path(path2, os2)) == (path1 == path2)


@pytest.mark.parametrize("path,os", all_paths)
@pytest.mark.parametrize("other", non_models + all_paths_str)
def test_not_equal(path : str, os : OS, other : Any):
    assert Path(path, os) != other

## HASH

@pytest.mark.parametrize("path,os,expected", map_hashes)
def test_hash(path : str, os : OS, expected : int):
    assert hash(Path(path, os)) == expected

## REPR

@pytest.mark.parametrize("path,os,expected", map_repr)
def test_repr(path : str, os : OS, expected : str):
    print(repr(Path(path, os)))
    print(expected)
    assert repr(Path(path, os)) == expected
