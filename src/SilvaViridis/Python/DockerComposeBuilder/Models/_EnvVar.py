from pydantic import BaseModel, ConfigDict, Field, validate_call
from typing import Any, Literal

from SilvaViridis.Python.Common.Text import NonEmptyString

from ..Common import ConfigurationDict

class EnvVar(BaseModel):
    name : NonEmptyString
    default_value : NonEmptyString | Literal[""] | None = Field(default = None)

    model_config = ConfigDict(
        frozen = True,
    )

    @validate_call
    def get_full_env_var(
        self,
        constainer_name : str,
    ) -> ConfigurationDict:
        return {
            self.name: f"${{{constainer_name}__{self.name}}}" \
                if self.default_value is None \
                else self.default_value,
        }

    def __eq__(
        self,
        other: Any,
    ) -> bool:
        return (
            isinstance(other, EnvVar)
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
            "default_value" : self.default_value,
        })
