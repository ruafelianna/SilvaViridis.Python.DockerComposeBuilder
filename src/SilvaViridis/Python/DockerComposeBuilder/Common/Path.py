from __future__ import annotations

from collections.abc import Callable
from ntpath import join as nt_path_join
from posixpath import join as posix_path_join
from pydantic import validate_call
from typing import Annotated, Any

from SilvaViridis.Python.Common.Collections import NonEmptySequence
from SilvaViridis.Python.Common.Text import NonEmptyString
from SilvaViridis.Python.Common.Validation import create_validator

from .OS import OS

class Path:
    @validate_call
    def __init__(
        self,
        path : NonEmptyString,
        os : OS = OS.POSIX,
    ):
        self._path = path
        self._os = os

    @property
    def path(
        self,
    ) -> str:
        return self._path

    @property
    def os(
        self,
    ) -> OS:
        return self._os

    @staticmethod
    def join(
        os : OS,
        paths : NonEmptySequence[PathTypeHint | NonEmptyString],
    ) -> str:
        if any([p.os != os for p in paths if isinstance(p, Path)]):
            raise ValueError("Cannot combine path parts of different OS interfaces")
        join_func = Path._os_mapping[os]
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

    _os_mapping : dict[OS, Callable[..., str]] = {
        OS.NT: nt_path_join,
        OS.POSIX : posix_path_join,
    }

PathValidator = create_validator(Path)

type PathTypeHint = Annotated[Any, PathValidator]

Path.join = validate_call(Path.join)
