from pydantic import BaseModel, Field

from SilvaViridis.Python.Common.Text import NonEmptyString

from ..Common import ConfigurationDict
from ..Models import EnvVar, Image, Network, Port, Volume

class Services(BaseModel):
    environment : set[EnvVar] = Field(default = set())
    image : Image | None
    networks : set[Network] = Field(default = set())
    ports : set[Port] = Field(default = set())
    volumes : set[Volume] = Field(default = set())

    def get_full_services(
        self,
        container_name : NonEmptyString,
    ) -> ConfigurationDict:
        result : ConfigurationDict = {}

        if len(self.environment) > 0:
            result["environment"] = {k: v for e in self.environment for k, v in e.get_full_env_var(container_name).items()}

        if self.image is not None:
            result["image"] = self.image.get_full_image()

        if len(self.networks) > 0:
            result["networks"] = [e.get_full_network() for e in self.networks]

        if len(self.ports) > 0:
            result["ports"] = [e.get_full_port() for e in self.ports]

        if len(self.volumes) > 0:
            result["volumes"] = [e.get_full_volume(container_name) for e in self.volumes]

        return {
            "services": result,
        }
