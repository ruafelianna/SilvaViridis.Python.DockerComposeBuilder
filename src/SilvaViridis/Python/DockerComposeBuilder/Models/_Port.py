from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator, validate_call
from typing import Any, Literal

from SilvaViridis.Python.Common.Numbers import UInt16
from SilvaViridis.Python.Common.Text import NonEmptyString

from SilvaViridis.Python.DockerComposeBuilder.Common import AppProtocol, Configuration, ConfigurationDict, ConfigurationStr

type TPort = UInt16
type TPortRange = tuple[UInt16, UInt16]

class Port(BaseModel):
    container_port : TPort | TPortRange
    host_port : TPort | TPortRange | None = Field(default = None)
    host_ip : IPv4Address | IPv6Address | None = Field(default = None)
    protocol : Literal["tcp", "udp"] | None = Field(default = None)
    app_protocol : AppProtocol | None = Field(default = None)
    name : NonEmptyString | None = Field(default = None)
    mode : Literal["host", "ingress"] | None = Field(default = None)
    force_long_syntax : bool = Field(default = False)

    model_config = ConfigDict(
        frozen = True,
    )

    @field_validator("container_port", "host_port", mode = "after")
    @classmethod
    def check_port_range(
        cls,
        port : TPort | TPortRange | None,
    ) -> TPort | TPortRange | None:
        if isinstance(port, tuple)and port[0] >= port[1]:
            raise ValueError("The range end should be greater than the range start")
        return port

    @model_validator(mode = "after")
    def validate_port_ranges_combination(
        self,
    ) -> Port:
        if (
            isinstance(self.container_port, tuple)
            and isinstance(self.host_port, tuple)
        ):
            s1, e1 = self.container_port
            s2, e2 = self.host_port
            if e1 - s1 != e2 - s2:
                raise ValueError("Port ranges should be of equal length")
        elif (
            isinstance(self.container_port, tuple)
            and isinstance(self.host_port, int)
        ):
            raise ValueError("Cannot map single host port to multiple container ports")
        return self

    @validate_call
    def get_full_port(
        self,
    ) -> Configuration:
        if(
            self.force_long_syntax
            or self.app_protocol is not None
            or self.mode is not None
            or self.name is not None
        ):
            return self._get_long()
        else:
            return self._get_short()

    def __eq__(
        self,
        other: Any,
    ) -> bool:
        return (
            isinstance(other, Port)
            and self.container_port == other.container_port
        )

    def __hash__(
        self,
    ) -> int:
        return hash(self.container_port)

    def __repr__(
        self,
    ) -> str:
        return repr({
            "container_port": self.container_port,
            "host_port" : self.host_port,
            "host_ip" : self.host_ip,
            "protocol" : self.protocol,
            "app_protocol" : self.app_protocol,
            "name" : self.name,
            "mode" : self.mode,
            "force_long_syntax" : self.force_long_syntax,
        })

    @validate_call
    def _get_long(
        self,
    ) -> ConfigurationDict:
        result : ConfigurationDict = {
            "target" : self._port_to_str(self.container_port),
        }

        if self.host_port is not None:
            result["published"] = self._port_to_str(self.host_port)

        if self.host_ip is not None:
            result["host_ip"] = str(self.host_ip)

        if self.name is not None:
            result["name"] = self.name

        if self.protocol is not None:
            result["protocol"] = self.protocol

        if self.app_protocol is not None:
            result["app_protocol"] = self.app_protocol.name

        if self.mode is not None:
            result["mode"] = self.mode

        return result

    @staticmethod
    @validate_call
    def _port_to_str(
        port : TPort | TPortRange,
        postfix : str = "",
    ) -> str:
        return f"{port[0]}-{port[1]}{postfix}" \
            if isinstance(port, tuple) \
            else f"{port}{postfix}"

    @validate_call
    def _get_short(
        self,
    ) -> ConfigurationStr:
        host_ip = "" \
            if self.host_ip is None \
            else f"{self.host_ip}:"

        host_port = "" \
            if self.host_port is None \
            else self._port_to_str(self.host_port, ":")

        protocol = "" \
            if self.protocol is None \
            else f"/{self.protocol}"

        return f"{host_ip}{host_port}{self._port_to_str(self.container_port)}{protocol}"
