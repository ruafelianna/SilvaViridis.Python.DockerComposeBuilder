from pydantic import BaseModel, ConfigDict, Field, validate_call
from typing import Any

from ..Common import ConfigurationDict, SELinuxRelabelingOption

class VolumeBindOptions(BaseModel):
    propagation : bool | None = Field(default = None)
    create_host_path : bool | None = Field(default = None)
    selinux : SELinuxRelabelingOption | None = Field(default = None)

    model_config = ConfigDict(
        frozen = True,
    )

    @validate_call
    def get_full_options(
        self,
    ) -> ConfigurationDict:
        bind : ConfigurationDict = {}

        if self.propagation is not None:
            bind["propagation"] = str(self.propagation).lower()

        if self.create_host_path is not None:
            bind["create_host_path"] = str(self.create_host_path).lower()

        if self.selinux is not None:
            bind["selinux"] = self.selinux.value

        return bind

    def __eq__(
        self,
        other : Any,
    ) -> bool:
        return (
            isinstance(other, VolumeBindOptions)
            and self.propagation == other.propagation
            and self.create_host_path == other.create_host_path
            and self.selinux == other.selinux
        )

    def __hash__(
        self,
    ) -> int:
        return hash((
            self.propagation,
            self.create_host_path,
            self.selinux,
        ))

    def __repr__(
        self,
    ) -> str:
        return repr({
            "propagation": self.propagation,
            "create_host_path": self.create_host_path,
            "selinux": self.selinux,
        })
