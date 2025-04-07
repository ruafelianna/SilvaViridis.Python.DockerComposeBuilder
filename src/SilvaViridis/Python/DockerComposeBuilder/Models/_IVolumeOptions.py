from __future__ import annotations

from typing import Annotated, Any, Protocol, runtime_checkable

from SilvaViridis.Python.Common.Validation import create_validator__is_instance

from ..Common import Configuration

@runtime_checkable
class IVolumeOptions(Protocol):
    def get_full_options(
        self,
    ) -> Configuration: ...

IVolumeOptionsValidator = create_validator__is_instance((IVolumeOptions,))

type IVolumeOptionsTypeHint = Annotated[Any, IVolumeOptionsValidator]
