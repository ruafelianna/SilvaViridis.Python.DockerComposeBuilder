from __future__ import annotations

from pydantic import BaseModel, ConfigDict, validate_call
from typing import Any

from SilvaViridis.Python.Common.Text import NonEmptyString

from ..Common import Configuration

class Network(BaseModel):
    name : NonEmptyString

    model_config = ConfigDict(
        frozen = True,
    )

    @validate_call
    def get_full_network(
        self,
    ) -> Configuration:
        return self.name

    def __eq__(
        self,
        other: Any,
    ) -> bool:
        return (
            isinstance(other, Network)
            and self.name == other.name
        )

    def __hash__(
        self,
    ) -> int:
        return hash(self.name)

    def __repr__(
        self,
    ) -> str:
        return repr({
            "name": self.name,
        })
