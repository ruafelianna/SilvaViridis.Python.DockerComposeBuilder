from pydantic import BaseModel, ConfigDict
from yaml import dump as to_yaml

from .Common import ConfigurationDict
from .Models import Container, Network

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

        for container in self.containers:
            services[container.container_name] = container.get_full_container()

            for network in container.networks:
                networks.add(network)

        categories["services"] = services

        if len(networks) > 0:
            categories["networks"] = {n.name: {"external": "true"} for n in networks}

        return to_yaml(categories)
