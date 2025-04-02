from pydantic import validate_call
from typing import Any

from SilvaViridis.Python.Common.Numbers import PositiveInt
from SilvaViridis.Python.Common.Unix import UnixPermissions

from .IVolumeOptions import IVolumeOptions
from ..Common import Configuration

class VolumeTmpfsOptions(IVolumeOptions):
    @validate_call
    def __init__(
        self,
        /,
        size : PositiveInt | None = None,
        mode : UnixPermissions | None = None,
    ):
        self._size = size
        self._mode = mode

    @property
    def size(
        self,
    ) -> int | None:
        return self._size

    @property
    def mode(
        self,
    ) -> UnixPermissions | None:
        return self._mode

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
