from pydantic import BaseModel, ConfigDict
from yaml import Dumper, ScalarNode, dump as to_yaml, add_representer

from .Common import ConfigurationDict
from .Models import Container, Network, Volume, VolumeType

def str_presenter(dumper : Dumper, data : str) -> ScalarNode:
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='|')
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)

add_representer(str, str_presenter)

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
