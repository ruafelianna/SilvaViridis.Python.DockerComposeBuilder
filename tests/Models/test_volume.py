import pytest

from itertools import product
from pydantic import ValidationError
from random import choices as random_choices

from SilvaViridis.Python.Common.Text import NonEmptyString
from SilvaViridis.Python.Common.Unix import PermissionLevel

from SilvaViridis.Python.DockerComposeBuilder.Common import Configuration, OS, Path, SELinuxRelabelingOption
from SilvaViridis.Python.DockerComposeBuilder.Models import Volume, VolumeAccessMode, VolumeBindOptions, VolumeOptions, VolumeTmpfsOptions, VolumeType

from ..fixtures import (
    DCG_BASE_DATA_FOLDER,
    check_create_full,
    check_repr_full,
    create_obj_from_dict,
    create_unix_permission,
)

LABELS = ["target", "volume_type", "access_mode", "source", "consistency", "bind_options", "volume_options", "tmpfs_options", "force_long_syntax"]

type TTrg = Path
type TVmt = VolumeType
type TAcm = VolumeAccessMode
type TSrc = Path | NonEmptyString | None
type TCst = NonEmptyString | None
type TBno = VolumeBindOptions | None
type TVmo = VolumeOptions | None
type TTmp = VolumeTmpfsOptions | None
type TFls = bool
type TAll = tuple[TTrg, TVmt, TAcm, TSrc, TCst, TBno, TVmo, TTmp, TFls]
type TAllC = tuple[TTrg, TVmt, TAcm, TSrc, TCst, TBno, TVmo, TTmp, TFls, str]

def create(args : TAll) -> Volume:
    return create_obj_from_dict(Volume, LABELS, *args)

def valid(args : TAll) -> bool:
    _, volume_type, _, source, _, bind_options, _, tmpfs_options, _ = args

    if volume_type == VolumeType.tmpfs and source is not None:
        return False

    if (
        volume_type != VolumeType.tmpfs
        and (
            source is None
            or (
                tmpfs_options is not None
                and (
                    tmpfs_options.size is not None
                    or tmpfs_options.mode is not None
                )
            )
        )
    ):
        return False

    if volume_type == VolumeType.volume and not isinstance(source, str):
        return False

    if volume_type != VolumeType.volume and volume_type != VolumeType.tmpfs and isinstance(source, str):
        return False

    if (
        volume_type != VolumeType.bind
        and bind_options is not None
        and (
            bind_options.propagation is not None
            or bind_options.create_host_path is not None
            or bind_options.selinux is not None
        )
    ):
        return False

    return True

target_values = [
    Path(path = "some/posix/path", os = OS.POSIX),
]

volume_type_values = list(VolumeType)

access_mode_values = list(VolumeAccessMode)

source_values = [
    Path(path = "some\\nt\\path", os = OS.NT),
    "hello",
    None,
]

consistency_values = ["whatever", None]

bind_options_values = [
    VolumeBindOptions(),
    VolumeBindOptions(propagation = True),
    None,
]

volume_options_values = [
    VolumeOptions(),
    VolumeOptions(nocopy = False),
    None,
]

tmpfs_options_values = [
    VolumeTmpfsOptions(),
    VolumeTmpfsOptions(size = 12345),
    None,
]

force_long_syntax_values = [False]

prod_all = list(product(
    target_values,
    volume_type_values,
    access_mode_values,
    source_values,
    consistency_values,
    bind_options_values,
    volume_options_values,
    tmpfs_options_values,
    force_long_syntax_values,
))

valid_volumes = [t for t in prod_all if valid(t)]

invalid_volumes = [t for t in prod_all if not valid(t)]

double_prod = random_choices(list(product(valid_volumes, repeat = 2)), k = 100)

target = Path(path = "/some/posix/path", os = OS.POSIX)
volume_type_1 = VolumeType.bind
volume_type_2 = VolumeType.volume
volume_type_3 = VolumeType.tmpfs
access_mode_1 = VolumeAccessMode.read_write
access_mode_2 = VolumeAccessMode.read_only
source_1 = Path(path = "data", os = OS.NT)
source_2 = "volume_name"
container = "apple"
bind_options_1 = VolumeBindOptions(selinux = SELinuxRelabelingOption.shared)
bind_options_2 = VolumeBindOptions(
    selinux = SELinuxRelabelingOption.private,
    create_host_path = False,
    propagation = True,
)
tmpfs_options_1 = VolumeTmpfsOptions(mode = create_unix_permission(PermissionLevel.rw, PermissionLevel.r, PermissionLevel.none))
tmpfs_options_2 = VolumeTmpfsOptions(size = None)
consistency = "whatever"
volume_options = VolumeOptions(nocopy = True, subpath = Path(path = "orange"))

full_volumes = [
    (
        (target, volume_type_1, access_mode_1, source_1, None, bind_options_1, None, None, False, container),
        f"{DCG_BASE_DATA_FOLDER}\\apple\\data:/some/posix/path:z"
    ),
    (
        (target, volume_type_1, access_mode_1, source_1, None, None, None, None, False, container),
        f"{DCG_BASE_DATA_FOLDER}\\apple\\data:/some/posix/path"
    ),
    (
        (target, volume_type_1, access_mode_1, source_1, None, bind_options_1, None, None, True, container),
        {
            "target": "/some/posix/path",
            "type": "bind",
            "source": f"{DCG_BASE_DATA_FOLDER}\\apple\\data",
            "bind": {
                "selinux": "z",
            },
        },
    ),
    (
        (target, volume_type_2, access_mode_2, source_2, None, None, None, None, False, container),
        f"volume_name:/some/posix/path:ro"
    ),
    (
        (target, volume_type_1, access_mode_2, source_1, None, bind_options_1, None, None, False, container),
        f"{DCG_BASE_DATA_FOLDER}\\apple\\data:/some/posix/path:ro,z"
    ),
    (
        (target, volume_type_3, access_mode_1, None, None, None, None, tmpfs_options_1, False, container),
        {
            "target" : "/some/posix/path",
            "type" : "tmpfs",
            "tmpfs": {
                "mode": "640",
            },
        },
    ),
    (
        (target, volume_type_1, access_mode_2, source_1, consistency, bind_options_2, volume_options, tmpfs_options_2, False, container),
        {
            "target": "/some/posix/path",
            "type": "bind",
            "read_only": "true",
            "consistency": "whatever",
            "source": f"{DCG_BASE_DATA_FOLDER}\\apple\\data",
            "bind": {
                "propagation": "true",
                "create_host_path": "false",
                "selinux": "Z",
            },
            "volume": {
                "nocopy": "true",
                "subpath": "orange",
            },
        },
    ),
]

## CREATION

@pytest.mark.parametrize("volume", valid_volumes)
def test_create(volume : TAll):
    check_create_full(LABELS, volume, create)


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("volume", invalid_volumes)
def test_create_fail(volume : TAll):
    create(volume)

## API

@pytest.mark.parametrize("volume,expected", full_volumes)
def test_full_volume(volume : TAllC, expected : Configuration):
    _, _, _, _, _, _, _, _, _, container_name = volume
    assert create(volume[:-1]).get_full_volume(container_name) == expected

## EQUALITY

@pytest.mark.parametrize("volume1,volume2", double_prod)
def test_equal(volume1 : TAll, volume2 : TAll):
    target1, _, _, _, _, _, _, _, _ = volume1
    target2, _, _, _, _, _, _, _, _ = volume2
    assert (create(volume1) == create(volume2)) == (target1 == target2)

## HASH

@pytest.mark.parametrize("volume", valid_volumes)
def test_hash(volume : TAll):
    target, _, _, _, _, _, _, _, _ = volume
    assert hash(create(volume)) == hash(target)

## REPR

@pytest.mark.parametrize("volume", valid_volumes)
def test_repr(volume : TAll):
    check_repr_full(LABELS, volume, create)
