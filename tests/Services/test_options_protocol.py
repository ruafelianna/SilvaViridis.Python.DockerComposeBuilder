from SilvaViridis.Python.DockerComposeBuilder.Common import Configuration
from SilvaViridis.Python.DockerComposeBuilder.Services import IVolumeOptions

class SomeVolumeOptions:
    def get_full_options(
        self,
    ) -> Configuration:
        return NotImplemented # pragma: no cover

def test_runtime_checkable():
    assert isinstance(SomeVolumeOptions, IVolumeOptions)
