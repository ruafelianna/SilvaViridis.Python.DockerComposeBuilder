import pytest

from beartype.roar import BeartypeCallHintViolation
from itertools import product
from typing import Any

from SilvaViridis.Python.DockerComposeBuilder.Models import Image

from ..fixtures import empty, non_models

images = ["postgres", "nginx"]

versions = ["17.4", "1.23.4", None]

prod_image_version = list(product(images, versions))

prod_all = list(product(prod_image_version, repeat = 2))

full_images = [(i, v, f"{i}{"" if v is None else f":{v}"}") for i, v in prod_image_version]

full_images_only = [i[2] for i in full_images]

prod_empty_version = list(product(empty, versions))

map_hashes = [(i, v, hash((i, v))) for i, v in prod_image_version]

map_repr = [(i, v, f"{{'name': {repr(i)}, 'version': {repr(v)}}}") for i, v in prod_image_version]

## CREATION

@pytest.mark.parametrize("name,version", prod_image_version)
def test_create(name : str, version : str | None):
    img = Image(name, version)
    assert (img.name, img.version) == (name, version)


@pytest.mark.xfail(raises = BeartypeCallHintViolation)
@pytest.mark.parametrize("name,version", prod_empty_version)
def test_create_fail(name : str, version : str | None):
    Image(name, version)

## API

@pytest.mark.parametrize("name,version,expected", full_images)
def test_full_image(name : str, version : str | None, expected : str):
    assert Image(name, version).get_full_image() == {"image": expected}

## EQUALITY

@pytest.mark.parametrize("image1,image2", prod_all)
def test_equal(image1 : tuple[str, str | None], image2 : tuple[str, str | None]):
    name1, version1 = image1
    name2, version2 = image2
    assert (Image(name1, version1) == Image(name2, version2)) == (name1 == name2 and version1 == version2)


@pytest.mark.parametrize("name,version", prod_image_version)
@pytest.mark.parametrize("other", non_models + full_images_only)
def test_not_equal(name : str, version : str | None, other : Any):
    assert Image(name, version) != other

## HASH

@pytest.mark.parametrize("name,version,expected", map_hashes)
def test_hash(name : str, version : str | None, expected : int):
    assert hash(Image(name, version)) == expected

## REPR

@pytest.mark.parametrize("name,version,expected", map_repr)
def test_repr(name : str, version : str | None, expected : str):
    assert repr(Image(name, version)) == expected
