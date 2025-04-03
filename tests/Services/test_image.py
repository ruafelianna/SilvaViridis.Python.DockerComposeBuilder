import pytest

from itertools import product
from pydantic import ValidationError

from SilvaViridis.Python.DockerComposeBuilder.Common import Configuration, HashType
from SilvaViridis.Python.DockerComposeBuilder.Services import Image

type TImg = str
type TTag = str | None
type TReg = str | None
type TPrj = str | None
type TDjt = tuple[HashType, str] | None
type TAll = tuple[TImg, TTag, TReg, TPrj, TDjt]

images = ["postgres"]

tags = ["17.4", None]

registries = ["company.com:12345", None]

projects = ["banana", None]

digests = [
    (HashType.sha256, "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03"),
    None,
]

i0 = images[0]
t0 = tags[0]
d0 : tuple[HashType, str] = digests[0] # type: ignore
p0 = projects[0]
r0 = registries[0]

full_images = [
    ((i0, None, None, None, None), i0),
    ((i0, t0, None, None, None), f"{i0}:{t0}"),
    ((i0, None, None, None, d0), f"{i0}@{d0[0]}:{d0[1]}"),
    ((i0, None, None, p0, None), f"{p0}/{i0}"),
    ((i0, None, r0, p0, None), f"{r0}/{p0}/{i0}"),
]

prod_all = list(product(images, tags, registries, projects, digests))

def create(image : TImg, tag : TTag, registry : TReg, project : TPrj, digest : TDjt):
    return Image(
        image = image,
        tag = tag,
        registry = registry,
        project = project,
        digest = digest,
    )

def valid(image : TImg, tag : TTag, registry : TReg, project : TPrj, digest : TDjt) -> bool:
    return tag is None or digest is None

valid_images = [t for t in prod_all if valid(*t)]

invalid_images = [t for t in prod_all if not valid(*t)]

## CREATION

@pytest.mark.parametrize("img", valid_images)
def test_create(img : TAll):
    img_obj = create(*img)
    assert (
        img_obj.image,
        img_obj.tag,
        img_obj.registry,
        img_obj.project,
        img_obj.digest,
    ) == img


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("img", invalid_images)
def test_create_fail(img : TAll):
    create(*img)

## API

@pytest.mark.parametrize("img,expected", full_images)
def test_full_image(img : TAll, expected : Configuration):
    assert create(*img).get_full_image() == {"image": expected}

## EQUALITY

@pytest.mark.parametrize("img1", valid_images)
@pytest.mark.parametrize("img2", valid_images)
def test_equal(img1 : TAll, img2 : TAll):
    assert (create(*img1) == create(*img2)) == (img1 == img2)

## HASH

@pytest.mark.parametrize("img", valid_images)
def test_hash(img : TAll):
    assert hash(create(*img)) == hash(img)

## REPR

@pytest.mark.parametrize("img", valid_images)
def test_repr(img : TAll):
    image, tag, registry, project, digest = img
    assert repr(create(*img)) == f"{{'image': {repr(image)}, 'tag': {repr(tag)}, 'registry': {repr(registry)}, 'project': {repr(project)}, 'digest': {repr(digest)}}}"
