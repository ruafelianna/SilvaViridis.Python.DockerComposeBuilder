from typing import Any, Literal

from SilvaViridis.Python.Common.Types import NonEmptyString

from ..Types import ConfDict

class EnvVar:
    def __init__(
        self,
        name : NonEmptyString,
        default_value : NonEmptyString | Literal[""] | None = None,
    ):
        self._name = name
        self._default_value = default_value

    @property
    def name(
        self,
    ) -> str:
        return self._name

    @property
    def default_value(
        self,
    ) -> str | None:
        return self._default_value

    def get_full_env_var(
        self,
        constainer_name : str,
    ) -> ConfDict:
        value = f"${{{constainer_name}__{self.name}}}" \
            if self.default_value is None \
            else self.default_value
        return {
            self.name: value,
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
