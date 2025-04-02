from pydantic import BaseModel, ConfigDict, Field, validate_call
from typing import Any

from SilvaViridis.Python.Common.Numbers import PositiveInt
from SilvaViridis.Python.Common.Unix import UnixPermissions

from ..Common import Configuration

class VolumeTmpfsOptions(BaseModel):
    size : PositiveInt | None = Field(default = None)
    mode : UnixPermissions | None = Field(default = None)

    model_config = ConfigDict(
        frozen = True,
    )

    @validate_call
    def get_full_options(
        self,
    ) -> Configuration:
        tmpfs : Configuration = {}

        if self.size is not None:
            tmpfs["size"] = str(self.size)

        if self.mode is not None:
            tmpfs["mode"] = self.mode.as_octal()

        return tmpfs

    def __eq__(
        self,
        other : Any,
    ) -> bool:
        return (
            isinstance(other, VolumeTmpfsOptions)
            and self.size == other.size
            and self.mode == other.mode
        )

    def __hash__(
        self,
    ) -> int:
        return hash((
            self.size,
            self.mode,
        ))

    def __repr__(
        self,
    ) -> str:
        return repr({
            "size": self.size,
            "mode": self.mode,
        })
