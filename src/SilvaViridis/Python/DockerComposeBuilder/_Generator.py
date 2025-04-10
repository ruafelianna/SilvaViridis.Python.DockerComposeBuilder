from pydantic import BaseModel, ConfigDict
from yaml import dump as to_yaml

from .Common import ConfigurationDict
from .Models import Container, Network, Volume, VolumeType

class DockerComposeGenerator(BaseModel):
    containers : frozenset[Container]

    model_config = ConfigDict(
        frozen = True,
    )

    def generate(
        self,
    ) -> str:
        categories : ConfigurationDict = {}
        services : ConfigurationDict = {}
        networks : set[Network] = set()
        volumes : set[Volume] = set()

        for container in self.containers:
            services[container.container_name] = container.get_full_container()

            for network in container.networks:
                networks.add(network)

            for volume in container.volumes:
                if volume.volume_type == VolumeType.volume:
                    volumes.add(volume)

        categories["services"] = services

        if len(networks) > 0:
            categories["networks"] = {n.name: {"external": "true"} for n in networks}

        if len(volumes) > 0:
            categories["volumes"] = {str(v.source): "" for v in volumes}

        return to_yaml(categories)
