from os.path import join as join_path
from pydantic import BaseModel, ConfigDict
from yaml import dump as to_yaml

from .Common import ConfigurationDict
from .Config import PathsConfig
from .Models import Container, Network

class Generator(BaseModel):
    containers : frozenset[Container]

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

        hosts : list[str] = []

        for container in self.containers:
            services[container.container_name] = container.get_full_container()

            for network in container.networks:
                networks.add(network)

            for env_var in container.environment:
                 if env_var.default_value is None:
                      value = container.get_env_var(env_var.name)
                      value = value[2:-1]
                      env.append(f"{value}=")

            hosts.append(f"127.0.0.1 {container.get_hostname()}")

        env = sorted(env)
        hosts = sorted(hosts)

        categories["services"] = services

        if len(networks) > 0:
            categories["networks"] = {n.name: {"external": "true"} for n in networks}

        output_folder = PathsConfig.YmlOutputFolder()

        with open(join_path(output_folder, "docker-compose.yml"), "w") as fd:
            fd.write(to_yaml(categories))

        with open(join_path(output_folder, ".env.sample"), "w") as fd:
             fd.write("\n".join(env) + "\n")

        with open(join_path(output_folder, "hosts.txt"), "w") as fd:
             fd.write("\n".join(hosts) + "\n")
