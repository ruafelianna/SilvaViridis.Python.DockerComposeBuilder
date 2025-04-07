from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator, validate_call
from typing import Any

from SilvaViridis.Python.Common.Text import NonEmptyString

from .IVolumeOptions import IVolumeOptions, IVolumeOptionsTypeHint
from .VolumeAccessMode import VolumeAccessMode
from .VolumeBindOptions import VolumeBindOptions
from .VolumeOptions import VolumeOptions
from .VolumeTmpfsOptions import VolumeTmpfsOptions
from .VolumeType import VolumeType
from ..Common import Configuration, Path
from ..Config import PathsConfig

@validate_call
def _check_options(
    options : IVolumeOptionsTypeHint | None
) -> Configuration | None:
    if isinstance(options,IVolumeOptions):
        category = options.get_full_options()
        return category if len(category) > 0 else None
    return None

class Volume(BaseModel):
    target : Path
    volume_type : VolumeType
    access_mode : VolumeAccessMode = Field(default = VolumeAccessMode.read_write)
    source : Path | NonEmptyString | None = Field(default = None)
    consistency : NonEmptyString | None = Field(default = None)
    bind_options : VolumeBindOptions | None = Field(default = None)
    volume_options : VolumeOptions | None = Field(default = None)
    tmpfs_options : VolumeTmpfsOptions | None = Field(default = None)
    force_long_syntax : bool = Field(default = False)

    model_config = ConfigDict(
        frozen = True,
    )

    @model_validator(mode = "after")
    def validate_volume_type_source(
        self,
    ) -> Volume:
        if (
            self.volume_type == VolumeType.tmpfs
            and self.source is not None
        ):
            raise ValueError("tmpfs mode doesn't support setting the source")

        if (
            self.volume_type != VolumeType.tmpfs
            and self.source is None
        ):
            raise ValueError("The source should be set")

        if (
            self.volume_type == VolumeType.volume
            and not isinstance(self.source, str)
        ):
            raise ValueError("Volume mode supports only str source")

        if (
            self.volume_type != VolumeType.volume
            and isinstance(self.source, str)
        ):
            raise ValueError("Only volume mode supports str source")

        return self

    @model_validator(mode = "after")
    def check_options(
        self,
    ) -> Volume:
        self._cat_bind = _check_options(self.bind_options)

        if (
            self.volume_type != VolumeType.bind
            and self._cat_bind is not None
        ):
            raise ValueError("Bind options shouldn't be set in the non-bind mode")

        self._cat_tmpfs = _check_options(self.tmpfs_options)

        if (
            self.volume_type != VolumeType.tmpfs
            and self._cat_tmpfs is not None
        ):
            raise ValueError("Tmpfs options shouldn't be set in the non-tmpfs mode")

        self._cat_volume = _check_options(self.volume_options)

        return self

    @staticmethod
    @validate_call
    def get_full_source(
        source : Path,
        container_name : NonEmptyString,
    ) -> str:
        return Path.join(
            source.os,
            (
                PathsConfig.BaseDataFolder,
                container_name,
                source,
            )
        )

    @validate_call
    def get_full_volume(
        self,
        container_name : NonEmptyString,
    ) -> Configuration:
        if isinstance(self.source, Path):
            source = self.get_full_source(self.source, container_name)
        elif isinstance(self.source, str):
            source = self.source
        else:
            source = ""

        if (
            self.force_long_syntax
            or self.volume_type not in [VolumeType.bind, VolumeType.volume]
            or self.consistency is not None
            or (
                self._cat_bind is not None
                and self.bind_options is not None
                and (
                    self.bind_options.propagation
                    or self.bind_options.create_host_path
                )
            )
            or self._cat_volume is not None
        ):
            return self._get_long(source)
        else:
            return self._get_short(source)

    def __eq__(
        self,
        other: Any,
    ) -> bool:
        return (
            isinstance(other, Volume)
            and self.target == other.target
        )

    def __hash__(
        self,
    ) -> int:
        return hash(self.target)

    def __repr__(
        self,
    ) -> str:
        return repr({
            "target": self.target,
            "volume_type": self.volume_type,
            "access_mode": self.access_mode,
            "source": self.source,
            "consistency": self.consistency,
            "bind_options": self.bind_options,
            "volume_options": self.volume_options,
            "tmpfs_options": self.tmpfs_options,
            "force_long_syntax": self.force_long_syntax,
        })

    @validate_call
    def _get_short(
        self,
        source : str,
    ) -> Configuration:
        access = "" \
            if self.access_mode == VolumeAccessMode.read_write \
            else self.access_mode.value

        selinux = self.bind_options.selinux.value \
            if self.bind_options is not None and self.bind_options.selinux is not None \
            else ""

        mode = self._combine_access_and_selinux(access, selinux)

        return f'{source}:{self.target}{mode}'

    @staticmethod
    @validate_call
    def _combine_access_and_selinux(
        access : str,
        selinux : str,
    ) -> str:
        if access == "" and selinux == "":
            return ""
        elif access != "" and selinux != "":
            return f":{access},{selinux}"
        elif access != "":
            return f":{access}"
        else:
            return f":{selinux}"

    @validate_call
    def _get_long(
        self,
        source : str,
    ) -> Configuration:
        result : Configuration = {
            "type": self.volume_type.name,
            "target": self.target.path,
        }

        if self.access_mode == VolumeAccessMode.read_only:
            result["read_only"] = "true"

        if self.consistency is not None:
            result["consistency"] = self.consistency

        if self.volume_type == VolumeType.tmpfs:
            if self._cat_tmpfs is not None:
                result["tmpfs"] = self._cat_tmpfs
        else:
            result["source"] = source

        if self._cat_bind is not None:
            result["bind"] = self._cat_bind

        if self._cat_volume is not None:
            result["volume"] = self._cat_volume

        return result
