from os import getenv
from typing import Any

DCG_BASE_DATA_FOLDER = getenv("DCG_BASE_DATA_FOLDER")
DCG_BASE_DOMAIN = getenv("DCG_BASE_DOMAIN")

empty = ["", "\n", "\t", " ", None]

non_models : list[Any] = [None, 123, object(), 4.2, list()]

containers = ["some", "container", "name"]
