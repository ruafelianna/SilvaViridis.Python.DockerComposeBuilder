from pydantic import validate_call
from typing import Any

from .IVolumeOptions import IVolumeOptions
from ..Common import Configuration, SELinuxRelabelingOption

class VolumeBindOptions(IVolumeOptions):
    @validate_call
    def __init__(
        self,
        /,
        propagation : bool | None = None,
        create_host_path : bool | None = None,
        selinux : SELinuxRelabelingOption | None = None,
    ):
        self._propagation = propagation
        self._create_host_path = create_host_path
        self._selinux = selinux

    @property
    def propagation(
        self,
    ) -> bool | None:
        return self._propagation

    @property
    def create_host_path(
        self,
    ) -> bool | None:
        return self._create_host_path

    @property
    def selinux(
        self,
    ) -> SELinuxRelabelingOption | None:
        return self._selinux

    @validate_call
    def get_full_options(
        self,
    ) -> Configuration:
        bind : Configuration = {}

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
