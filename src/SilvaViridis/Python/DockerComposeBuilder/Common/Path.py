from __future__ import annotations

from collections.abc import Callable
from ntpath import join as nt_path_join
from posixpath import join as posix_path_join
from pydantic import BaseModel, ConfigDict, Field, validate_call
from typing import Annotated, Any

from SilvaViridis.Python.Common.Collections import NonEmptySequence
from SilvaViridis.Python.Common.Text import NonEmptyString
from SilvaViridis.Python.Common.Validation import create_validator__is_instance

from .OS import OS

_os_mapping : dict[OS, Callable[..., str]] = {
    OS.NT: nt_path_join,
    OS.POSIX : posix_path_join,
}

class Path(BaseModel):
    path : NonEmptyString
    os : OS = Field(default = OS.POSIX)

    model_config = ConfigDict(
        frozen = True,
    )

    @staticmethod
    def join(
        os : OS,
        paths : NonEmptySequence[PathTypeHint | NonEmptyString],
    ) -> str:
        if any([p.os != os for p in paths if isinstance(p, Path)]):
            raise ValueError("Cannot combine path parts of different OS interfaces")
        join_func = _os_mapping[os]
        return join_func(*(str(p) for p in paths))

    def __str__(
        self,
    ) -> str:
        return self.path

    def __eq__(
        self,
        other: Any,
    ) -> bool:
        return (
            isinstance(other, Path)
            and self.path == other.path
        )

    def __hash__(
        self,
    ) -> int:
        return hash(self.path)

    def __repr__(
        self,
    ) -> str:
        return repr({
            "path": self.path,
            "os" : self.os,
        })

PathValidator = create_validator__is_instance((Path,))

type PathTypeHint = Annotated[Any, PathValidator]

Path.join = validate_call(Path.join)
