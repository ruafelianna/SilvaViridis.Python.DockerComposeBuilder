from typing import Any

from SilvaViridis.Python.Common.Types import NonEmptyString

from ..Types import ConfDict

class Image:
    def __init__(
        self,
        name : NonEmptyString,
        version : NonEmptyString | None = None,
    ):
        self._name = name
        self._version = version

    @property
    def name(
        self,
    ) -> str:
        return self._name

    @property
    def version(
        self,
    ) -> str | None:
        return self._version

    def get_full_image(
        self,
    ) -> ConfDict:
        value = self.name \
            if self.version is None \
            else f"{self.name}:{self.version}"
        return {
            "image": value,
        }

    def __eq__(
        self,
        other: Any,
    ) -> bool:
        return (
            isinstance(other, Image)
            and self.name == other.name
            and self.version == other.version
        )

    def __hash__(
        self,
    ) -> int:
        return hash((self.name, self.version))

    def __repr__(
        self,
    ) -> str:
        return repr({
            "name": self.name,
            "version" : self.version,
        })
