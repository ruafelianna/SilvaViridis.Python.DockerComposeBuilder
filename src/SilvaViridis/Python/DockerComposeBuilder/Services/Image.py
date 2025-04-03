from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Any

from SilvaViridis.Python.Common.Text import NonEmptyString

from ..Common import Configuration, HashType

class Image(BaseModel):
    image : NonEmptyString
    tag : NonEmptyString | None = Field(default = None)
    registry : NonEmptyString | None = Field(default = None)
    project : NonEmptyString | None = Field(default = None)
    digest : tuple[HashType, NonEmptyString] | None = Field(default = None)

    model_config = ConfigDict(
        frozen = True,
    )

    @model_validator(mode = "after")
    def validate_only_tag_or_digest(
        self,
    ) -> Image:
        if self.tag is not None and self.digest is not None:
            raise ValueError("Cannot set both tag and digest")
        return self

    def get_full_image(
        self,
    ) -> Configuration:
        registry = "" if self.registry is None else f"{self.registry}/"
        project = "" if self.project is None else f"{self.project}/"
        tag = "" if self.tag is None else f":{self.tag}"
        digest = "" if self.digest is None else f"@{self.digest[0]}:{self.digest[1]}"
        return {
            "image": f"{registry}{project}{self.image}{tag}{digest}",
        }

    def __eq__(
        self,
        other: Any,
    ) -> bool:
        return (
            isinstance(other, Image)
            and self.image == other.image
            and self.tag == other.tag
            and self.registry == other.registry
            and self.project == other.project
            and self.digest == other.digest
        )

    def __hash__(
        self,
    ) -> int:
        return hash((self.image, self.tag, self.registry, self.project, self.digest))

    def __repr__(
        self,
    ) -> str:
        return repr({
            "image": self.image,
            "tag" : self.tag,
            "registry" : self.registry,
            "project" : self.project,
            "digest" : self.digest,
        })
