from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, validate_call
from typing import Any

from ..Common import Configuration, Path

class VolumeOptions(BaseModel):
    nocopy : bool | None = Field(default = None)
    subpath : Path | None = Field(default = None)

    model_config = ConfigDict(
        frozen = True,
    )

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
