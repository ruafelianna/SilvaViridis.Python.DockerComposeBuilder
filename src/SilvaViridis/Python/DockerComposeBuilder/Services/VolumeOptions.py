from __future__ import annotations

from pydantic import validate_call
from typing import Any

from .IVolumeOptions import IVolumeOptions
from ..Common import Configuration, PathTypeHint

class VolumeOptions(IVolumeOptions):
    @validate_call
    def __init__(
        self,
        /,
        nocopy : bool | None = None,
        subpath : PathTypeHint | None = None,
    ) -> None:
        self._nocopy = nocopy
        self._subpath = subpath

    @property
    def nocopy(
        self,
    ) -> bool | None:
        return self._nocopy

    @property
    def subpath(
        self,
    ) -> PathTypeHint | None:
        return self._subpath

    @validate_call
    def get_full_options(
        self,
    ) -> Configuration:
        volume : Configuration = {}

        if self.nocopy is not None:
            volume["nocopy"] = str(self.nocopy).lower()

        if self.subpath is not None:
            volume["subpath"] = self.subpath.path

        return volume

    def __eq__(
        self,
        other : Any,
    ) -> bool:
        return (
            isinstance(other, VolumeOptions)
            and self.nocopy == other.nocopy
            and self.subpath == other.subpath
        )

    def __hash__(
        self,
    ) -> int:
        return hash((
            self.nocopy,
            self.subpath,
        ))

    def __repr__(
        self,
    ) -> str:
        return repr({
            "nocopy": self.nocopy,
            "subpath": self.subpath,
        })
