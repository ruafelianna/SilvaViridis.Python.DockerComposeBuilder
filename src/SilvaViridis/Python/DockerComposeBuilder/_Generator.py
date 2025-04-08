from os.path import join as join_path
from pydantic import BaseModel, ConfigDict
from yaml import dump as to_yaml

from ._Container import Container
from .Common import ConfigurationDict
from .Config import PathsConfig
from .Models import Network

class Generator(BaseModel):
    containers : set[Container]

    model_config = ConfigDict(
        frozen = True,
    )

    def generate(
        self,
    ) -> None:
        categories : ConfigurationDict = {}

        services : ConfigurationDict = {}

        networks : set[Network] = set()

        env : list[str] = []

        for container in self.containers:
            services[container.container_name] = container.get_full_container()

            for network in container.networks:
                networks.add(network)

            for env_var in container.environment:
                 if env_var.default_value is None:
                      value = container.get_env_var(env_var.name)
                      value = value[2:-1]
                      env.append(f"{value}=")

        categories["services"] = services

        if len(networks) > 0:
            categories["networks"] = {n.name: {"external": "true"} for n in networks}

        with open(join_path(PathsConfig.YmlOutputFolder, f"docker-compose.yml"), "w") as fd:
            fd.write(to_yaml(categories))

        with open(join_path(PathsConfig.YmlOutputFolder, f".env.sample"), "w") as fd:
             fd.write("\n".join(env) + "\n")
