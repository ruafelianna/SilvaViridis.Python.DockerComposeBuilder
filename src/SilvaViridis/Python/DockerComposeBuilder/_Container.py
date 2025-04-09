from __future__ import annotations

from pydantic import BaseModel, Field, validate_call
from typing import Any

from SilvaViridis.Python.Common.Text import NonEmptyString

from SilvaViridis.Python.DockerComposeBuilder.Common import ConfigurationDict, ConfigurationTuple

from .Config import NetworkConfig
from .Models import Build, EnvVar, Image, Network, Port, RestartPolicy, Volume

class Container(BaseModel):
    build : Build | None = Field(default = None)
    command : NonEmptyString | None = Field(default = None)
    container_name : NonEmptyString
    depends_on : set[Container] = Field(default = set())
    environment : set[EnvVar] = Field(default = set())
    environment_other : dict[Container, set[EnvVar]] = Field(default = {})
    hostname : NonEmptyString | None = Field(default = None)
    image : Image | None = Field(default = None)
    networks : set[Network] = Field(default = set())
    ports : set[Port] = Field(default = set())
    restart : RestartPolicy | None = Field(default = None)
    volumes : set[Volume] = Field(default = set())

    def __eq__(
        self,
        other : Any,
    ) -> bool:
        return (
            isinstance(other, Container)
            and self.container_name == other.container_name
        )

    def __hash__(
        self,
    ) -> int:
        return hash(self.container_name)

    @validate_call
    def get_env_var(
        self,
        name : NonEmptyString,
    ) -> str:
        for e in self.environment:
            if e.name == name:
                return self._get_env_var_value(e)[1]
        raise ValueError(f"There is no env_var <{name}> in container <{self.container_name}>")

    @validate_call
    def get_hostname(
        self,
    ) -> str:
        return f"{self.container_name if self.hostname is None else self.hostname}.{NetworkConfig.BaseDomainName}"

    @validate_call
    def get_full_container(
        self,
    ) -> ConfigurationDict:
        services : ConfigurationDict = {
            "container_name": self.container_name,
            "hostname": self.get_hostname(),
        }

        if self.build is not None:
            services["build"] = self.build.get_full_build()

        if self.command is not None:
            services["command"] = self.command

        if len(self.depends_on) > 0:
            services["depends_on"] = [d.container_name for d in self.depends_on]

        if len(self.environment) > 0:
            services["environment"] = {}

            for env_var in self.environment:
                var = self._get_env_var_value(env_var)
                services["environment"][var[0]] = var[1]

        if self.image is not None:
            services["image"] = self.image.get_full_image()

        if len(self.networks) > 0:
            services["networks"] = [e.get_full_network() for e in self.networks]

        if len(self.ports) > 0:
            services["ports"] = [e.get_full_port() for e in self.ports]

        if self.restart is not None:
            services["restart"] = self.restart.value

        if len(self.volumes) > 0:
            services["volumes"] = [e.get_full_volume(self.container_name) for e in self.volumes]

        return services

    @validate_call
    def _get_env_var_value(
        self,
        env_var : EnvVar,
    ) -> ConfigurationTuple[str]:
        return env_var.get_full_env_var(self.container_name)
