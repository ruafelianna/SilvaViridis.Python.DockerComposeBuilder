import pytest

from pydantic import ValidationError

from SilvaViridis.Python.Common.Unix import PermissionLevel, UnixPermissions

from SilvaViridis.Python.DockerComposeBuilder.Common import OS, Path, SELinuxRelabelingOption
from SilvaViridis.Python.DockerComposeBuilder.Services import Volume, VolumeAccessMode, VolumeBindOptions, VolumeOptions, VolumeTmpfsOptions, VolumeType

from ..fixtures import DCG_BASE_DATA_FOLDER, containers, empty

targets = ["some/posix/path"]

map_targets = [Path(path = t, os = OS.POSIX) for t in targets]

path_sources_nt = ["some\\nt\\path"]

map_sources_nt = [Path(path = s, os = OS.NT) for s in path_sources_nt]

path_sources_posix = ["another/posix/path"]

map_sources_posix = [Path(path = s, os = OS.POSIX) for s in path_sources_posix]

name_sources = ["hello"]

all_sources = map_sources_nt + map_sources_posix + name_sources

sizes = [12345]

consistencies = ["whatever"]

subpaths = ["sunny"]

permissions = [
    (PermissionLevel.rw, PermissionLevel.none, PermissionLevel.wx),
    (PermissionLevel.x, PermissionLevel.r, PermissionLevel.rx),
    (PermissionLevel.r, PermissionLevel.rwx, PermissionLevel.none),
    (PermissionLevel.none, PermissionLevel.w, PermissionLevel.w),
    (PermissionLevel.wx, PermissionLevel.rwx, PermissionLevel.rwx),
]

unix_permissions = [UnixPermissions(user = u, group = g, other = o) for u, g, o in permissions]

## CREATION

@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_nt + map_sources_posix)
@pytest.mark.parametrize("access_mode", VolumeAccessMode)
def test_create_short(target : Path, source : Path, access_mode : VolumeAccessMode):
    volume = Volume(
        target = target,
        volume_type = VolumeType.bind,
        access_mode = access_mode,
        source = source,
        bind_options = VolumeBindOptions(
            selinux = SELinuxRelabelingOption.shared,
        ),
    )
    assert (
        volume.target,
        volume.volume_type,
        volume.access_mode,
        volume.source,
        volume.consistency,
        volume.bind_options,
        volume.volume_options,
        volume.tmpfs_options,
        volume.force_long_syntax,
    ) == (
        target,
        VolumeType.bind,
        access_mode,
        source,
        None,
        VolumeBindOptions(
            selinux = SELinuxRelabelingOption.shared,
        ),
        None,
        None,
        False,
    )


@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_nt + map_sources_posix)
@pytest.mark.parametrize("access_mode", VolumeAccessMode)
def test_create_forced(target : Path, source : Path, access_mode : VolumeAccessMode):
    volume = Volume(
        target = target,
        volume_type = VolumeType.bind,
        access_mode = access_mode,
        source = source,
        bind_options = VolumeBindOptions(
            selinux = SELinuxRelabelingOption.private,
        ),
        force_long_syntax = True,
    )
    assert (
        volume.target,
        volume.volume_type,
        volume.access_mode,
        volume.source,
        volume.consistency,
        volume.bind_options,
        volume.volume_options,
        volume.tmpfs_options,
        volume.force_long_syntax,
    ) == (
        target,
        VolumeType.bind,
        access_mode,
        source,
        None,
        VolumeBindOptions(
            selinux = SELinuxRelabelingOption.private,
        ),
        None,
        None,
        True,
    )


@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_nt + map_sources_posix)
@pytest.mark.parametrize("access_mode", VolumeAccessMode)
@pytest.mark.parametrize("consistency", consistencies)
@pytest.mark.parametrize("subpath", subpaths)
def test_create_full(target : Path, source : Path, access_mode : VolumeAccessMode, consistency : str, subpath : str):
    volume = Volume(
        target = target,
        volume_type = VolumeType.bind,
        access_mode = access_mode,
        source = source,
        consistency = consistency,
        bind_options = VolumeBindOptions(
            propagation = False,
            create_host_path = True,
            selinux = SELinuxRelabelingOption.private,
        ),
        volume_options = VolumeOptions(
            nocopy = True,
            subpath = Path(path = subpath, os = source.os),
        ),
    )
    assert (
        volume.target,
        volume.volume_type,
        volume.access_mode,
        volume.source,
        volume.consistency,
        volume.bind_options,
        volume.volume_options,
        volume.tmpfs_options,
        volume.force_long_syntax,
    ) == (
        target,
        VolumeType.bind,
        access_mode,
        source,
        consistency,
        VolumeBindOptions(
            propagation = False,
            create_host_path = True,
            selinux = SELinuxRelabelingOption.private,
        ),
        VolumeOptions(
            nocopy = True,
            subpath = Path(path = subpath, os = source.os),
        ),
        None,
        False,
    )


@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_nt + map_sources_posix)
@pytest.mark.parametrize("access_mode", VolumeAccessMode)
@pytest.mark.parametrize("permission", unix_permissions)
@pytest.mark.parametrize("size", sizes)
@pytest.mark.parametrize("consistency", consistencies)
@pytest.mark.parametrize("subpath", subpaths)
def test_create_tmpfs(
    target : Path, source : Path, access_mode : VolumeAccessMode,
    permission : UnixPermissions, size : int, consistency : str, subpath : str,
):
    volume = Volume(
        target = target,
        volume_type = VolumeType.tmpfs,
        access_mode = access_mode,
        consistency = consistency,
        tmpfs_options = VolumeTmpfsOptions(
            size = size,
            mode = permission,
        ),
        volume_options = VolumeOptions(
            nocopy = True,
            subpath = Path(path = subpath, os = source.os),
        ),
        force_long_syntax = True,
    )
    assert (
        volume.target,
        volume.volume_type,
        volume.access_mode,
        volume.source,
        volume.consistency,
        volume.bind_options,
        volume.volume_options,
        volume.tmpfs_options,
        volume.force_long_syntax,
    ) == (
        target,
        VolumeType.tmpfs,
        access_mode,
        "",
        consistency,
        None,
        VolumeOptions(
            nocopy = True,
            subpath = Path(path = subpath, os = source.os),
        ),
        VolumeTmpfsOptions(
            size = size,
            mode = permission,
        ),
        True,
    )


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_nt + map_sources_posix)
def test_create_fail_tmpfs_and_source_set(target : Path, source : Path):
    Volume(
        target = target,
        volume_type = VolumeType.tmpfs,
        source = source,
    )


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("target", map_targets)
def test_create_fail_volume_and_source_not_str(target : Path):
    Volume(
        target = target,
        volume_type = VolumeType.volume,
        source = Path(path = "some/path"),
    )


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("target", map_targets)
def test_create_fail_no_voulme_and_source_str(target : Path):
    Volume(
        target = target,
        volume_type = VolumeType.npipe,
        source = "volume_name",
    )


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("target", map_targets)
def test_create_fail_no_tmpfs_and_source(target : Path):
    Volume(
        target = target,
        volume_type = VolumeType.npipe,
    )


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_nt + map_sources_posix)
def test_create_fail_bind_options_no_bind(target : Path, source : Path):
    Volume(
        target = target,
        volume_type = VolumeType.cluster,
        source = source,
        bind_options = VolumeBindOptions(
            propagation = True,
        ),
    )


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_nt + map_sources_posix)
@pytest.mark.parametrize("size", sizes)
def test_create_fail_tmpfs_options_no_tmpfs(target : Path, source : Path, size : int):
    Volume(
        target = target,
        volume_type = VolumeType.bind,
        source = source,
        tmpfs_options = VolumeTmpfsOptions(
            size = size,
        ),
    )

## API

@pytest.mark.parametrize("source", map_sources_nt)
@pytest.mark.parametrize("container_name", containers)
def test_full_source_nt(source : Path, container_name : str):
    assert Volume.get_full_source(source, container_name) == f"{DCG_BASE_DATA_FOLDER}\\{container_name}\\{source}"


@pytest.mark.parametrize("source", map_sources_posix)
@pytest.mark.parametrize("container_name", containers)
def test_full_source_posix(source : Path, container_name : str):
    assert Volume.get_full_source(source, container_name) == f"{DCG_BASE_DATA_FOLDER}/{container_name}/{source}"


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("source", map_sources_nt + map_sources_posix)
@pytest.mark.parametrize("container_name", empty)
def test_full_source_fail(source : Path, container_name : str):
    Volume.get_full_source(source, container_name)


@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_posix)
@pytest.mark.parametrize("access_mode", VolumeAccessMode)
@pytest.mark.parametrize("container_name", containers)
@pytest.mark.parametrize("selinux", SELinuxRelabelingOption)
def test_full_volume_short(target : Path, source : Path, access_mode : VolumeAccessMode, container_name : str, selinux : SELinuxRelabelingOption):
    volume = Volume(
        target = target,
        volume_type = VolumeType.bind,
        access_mode = access_mode,
        source = source,
        bind_options = VolumeBindOptions(
            selinux = selinux,
        ),
    )
    access = "ro," if access_mode == VolumeAccessMode.read_only else ""
    assert volume.get_full_volume(container_name) == f"{DCG_BASE_DATA_FOLDER}/{container_name}/{volume.source}:{volume.target}:{access}{selinux.value}"


@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_posix)
@pytest.mark.parametrize("access_mode", VolumeAccessMode)
@pytest.mark.parametrize("container_name", containers)
def test_full_volume_short_no_selinux(target : Path, source : Path, access_mode : VolumeAccessMode, container_name : str):
    volume = Volume(
        target = target,
        volume_type = VolumeType.bind,
        access_mode = access_mode,
        source = source,
    )
    access = ":ro" if access_mode == VolumeAccessMode.read_only else ""
    assert volume.get_full_volume(container_name) == f"{DCG_BASE_DATA_FOLDER}/{container_name}/{volume.source}:{volume.target}{access}"


@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_posix)
@pytest.mark.parametrize("access_mode", VolumeAccessMode)
@pytest.mark.parametrize("container_name", containers)
def test_full_volume_forced(target : Path, source : Path, access_mode : VolumeAccessMode, container_name : str):
    volume = Volume(
        target = target,
        volume_type = VolumeType.bind,
        access_mode = access_mode,
        source = source,
        bind_options = VolumeBindOptions(
            selinux = SELinuxRelabelingOption.private,
        ),
        force_long_syntax = True,
    )
    exprected = {
        "target": target.path,
        "type": VolumeType.bind.name,
        "source": f"{DCG_BASE_DATA_FOLDER}/{container_name}/{volume.source}",
        "bind": {
            "selinux": SELinuxRelabelingOption.private.value,
        },
    }
    if access_mode == VolumeAccessMode.read_only:
        exprected["read_only"] = "true"
    assert volume.get_full_volume(container_name) == exprected


@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_posix)
@pytest.mark.parametrize("access_mode", VolumeAccessMode)
@pytest.mark.parametrize("container_name", containers)
@pytest.mark.parametrize("consistency", consistencies)
@pytest.mark.parametrize("subpath", subpaths)
def test_full_volume_full(
    target : Path, source : Path, access_mode : VolumeAccessMode,
    container_name : str, consistency : str, subpath : str,
):
    volume = Volume(
        target = target,
        volume_type = VolumeType.bind,
        access_mode = access_mode,
        source = source,
        consistency = consistency,
        bind_options = VolumeBindOptions(
            propagation = False,
            create_host_path = True,
            selinux = SELinuxRelabelingOption.private,
        ),
        volume_options = VolumeOptions(
            nocopy = True,
            subpath = Path(path = subpath, os = source.os),
        ),
    )
    exprected = {
        "target": target.path,
        "type": VolumeType.bind.name,
        "source": f"{DCG_BASE_DATA_FOLDER}/{container_name}/{volume.source}",
        "consistency": consistency,
        "bind": {
            "propagation": "false",
            "create_host_path": "true",
            "selinux": SELinuxRelabelingOption.private.value,
        },
        "volume": {
            "nocopy": "true",
            "subpath": subpath,
        },
    }
    if access_mode == VolumeAccessMode.read_only:
        exprected["read_only"] = "true"
    assert volume.get_full_volume(container_name) == exprected


@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_nt + map_sources_posix)
@pytest.mark.parametrize("access_mode", VolumeAccessMode)
@pytest.mark.parametrize("permission", unix_permissions)
@pytest.mark.parametrize("container_name", containers)
@pytest.mark.parametrize("size", sizes)
@pytest.mark.parametrize("consistency", consistencies)
@pytest.mark.parametrize("subpath", subpaths)
def test_full_volume_tmpfs(
    target : Path, source : Path, access_mode : VolumeAccessMode, permission : UnixPermissions,
    container_name : str, size : int, consistency : str, subpath : str,
):
    volume = Volume(
        target = target,
        volume_type = VolumeType.tmpfs,
        access_mode = access_mode,
        consistency = consistency,
        tmpfs_options = VolumeTmpfsOptions(
            size = size,
            mode = permission,
        ),
        volume_options = VolumeOptions(
            nocopy = True,
            subpath = Path(path = subpath, os = source.os),
        ),
        force_long_syntax = True,
    )
    exprected = {
        "target": target.path,
        "type": VolumeType.tmpfs.name,
        "consistency": consistency,
        "tmpfs": {
            "size": str(size),
            "mode": permission.as_octal(),
        },
        "volume": {
            "nocopy": "true",
            "subpath": subpath,
        },
    }
    if access_mode == VolumeAccessMode.read_only:
        exprected["read_only"] = "true"
    assert volume.get_full_volume(container_name) == exprected

## EQUALITY

@pytest.mark.parametrize("target1", map_targets)
@pytest.mark.parametrize("target2", map_targets)
@pytest.mark.parametrize("source1", map_sources_nt + map_sources_posix)
@pytest.mark.parametrize("source2", name_sources)
@pytest.mark.parametrize("access_mode1", VolumeAccessMode)
@pytest.mark.parametrize("access_mode2", VolumeAccessMode)
def test_equal(
    target1 : Path, source1 : Path, access_mode1 : VolumeAccessMode,
    target2 : Path, source2 : Path, access_mode2 : VolumeAccessMode,
):
    volume1 = Volume(
        target = target1,
        volume_type = VolumeType.bind,
        access_mode = access_mode1,
        source = source1,
    )
    volume2 = Volume(
        target = target2,
        volume_type = VolumeType.volume,
        access_mode = access_mode2,
        source = source2,
    )
    assert (volume1 == volume2) == (target1 == target2)

## HASH

@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_nt + map_sources_posix)
@pytest.mark.parametrize("access_mode", VolumeAccessMode)
def test_hash(target : Path, source : Path, access_mode : VolumeAccessMode):
    volume = Volume(
        target = target,
        volume_type = VolumeType.bind,
        access_mode = access_mode,
        source = source,
    )
    assert hash(volume) == hash(target)

## REPR

@pytest.mark.parametrize("target", map_targets)
@pytest.mark.parametrize("source", map_sources_nt + map_sources_posix)
@pytest.mark.parametrize("access_mode", VolumeAccessMode)
def test_repr(target : Path, source : Path, access_mode : VolumeAccessMode):
    volume = Volume(
        target = target,
        volume_type = VolumeType.bind,
        access_mode = access_mode,
        source = source,
    )
    assert repr(volume) == f"{{'target': {repr(target)}, 'volume_type': {repr(VolumeType.bind)}, 'access_mode': {repr(access_mode)}, 'source': {repr(source)}, 'consistency': None, 'bind_options': None, 'volume_options': None, 'tmpfs_options': None, 'force_long_syntax': False}}"
