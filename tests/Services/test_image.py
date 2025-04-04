import pytest

from itertools import product
from pydantic import ValidationError

from SilvaViridis.Python.DockerComposeBuilder.Common import Configuration, HashType
from SilvaViridis.Python.DockerComposeBuilder.Services import Image

from ..fixtures import (
    check_create_full,
    check_repr_full,
    create_obj_from_dict,
)

LABELS = ["image", "tag", "registry", "project", "digest"]

type TImg = str
type TTag = str | None
type TReg = str | None
type TPrj = str | None
type TDjt = tuple[HashType, str] | None
type TAll = tuple[TImg, TTag, TReg, TPrj, TDjt]

def create(args : TAll) -> Image:
    return create_obj_from_dict(Image, LABELS, *args)

def valid(args : TAll) -> bool:
    _, tag, _, _, digest = args
    return tag is None or digest is None

image_values = ["postgres"]

tag_values = ["17.4", None]

registry_values = ["company.com:12345", None]

project_values = ["banana", None]

digest_values = [
    (HashType.sha256, "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03"),
    None,
]

prod_all = list(product(image_values, tag_values, registry_values, project_values, digest_values))

valid_images = [t for t in prod_all if valid(t)]

invalid_images = [t for t in prod_all if not valid(t)]

image = "postgres"
tag = "17.4"
digest = (HashType.sha256, "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03")
project = "banana"
registry = "company.com:12345"

full_images = [
    ((image, None, None, None, None), "postgres"),
    ((image, tag, None, None, None), "postgres:17.4"),
    ((image, None, None, None, digest), "postgres@sha256:5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03"),
    ((image, None, None, project, None), "banana/postgres"),
    ((image, None, registry, project, None), "company.com:12345/banana/postgres"),
]

## CREATION

@pytest.mark.parametrize("img", valid_images)
def test_create(img : TAll):
    img_obj = create(img)
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
    check_create_full(LABELS, img, create)

## API

@pytest.mark.parametrize("img,expected", full_images)
def test_full_image(img : TAll, expected : Configuration):
    assert create(img).get_full_image() == {"image": expected}

## EQUALITY

@pytest.mark.parametrize("img1", valid_images)
@pytest.mark.parametrize("img2", valid_images)
def test_equal(img1 : TAll, img2 : TAll):
    assert (create(img1) == create(img2)) == (img1 == img2)

## HASH

@pytest.mark.parametrize("img", valid_images)
def test_hash(img : TAll):
    assert hash(create(img)) == hash(img)

## REPR

@pytest.mark.parametrize("img", valid_images)
def test_repr(img : TAll):
    check_repr_full(LABELS, img, create)
