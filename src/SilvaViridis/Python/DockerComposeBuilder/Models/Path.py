from __future__ import annotations

from collections.abc import Callable
from ntpath import join as nt_path_join
from posixpath import join as posix_path_join
from typing import Any

from SilvaViridis.Python.Common.Types import NonEmptyString

from ..Enums import OS

class Path:
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

    _os_mapping : dict[OS, Callable[..., str]] = {
        OS.NT: nt_path_join,
        OS.POSIX : posix_path_join,
    }

    @staticmethod
    def join(
        os : OS,
        *paths : Path | NonEmptyString,
    ) -> str:
        if any([p.os != os for p in paths if isinstance(p, Path)]):
            raise ValueError("Cannot combine path parts of different file systems")
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
