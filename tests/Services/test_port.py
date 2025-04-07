import pytest

from ipaddress import IPv4Address, IPv6Address
from itertools import product
from pydantic import ValidationError
from random import choices as random_choices
from typing import Literal

from SilvaViridis.Python.DockerComposeBuilder.Common import AppProtocol, Configuration
from SilvaViridis.Python.DockerComposeBuilder.Services import Port, TPort, TPortRange

from ..fixtures import (
    check_create_full,
    check_repr_full,
    create_obj_from_dict,
)

LABELS = ["container_port", "host_port", "host_ip", "protocol", "app_protocol", "name", "mode", "force_long_syntax"]

type TCpt = TPort | TPortRange
type THpt = TPort | TPortRange | None
type THip = IPv4Address | IPv6Address | None
type TPrt = Literal["tcp", "udp"] | None
type TNme = str | None
type TApr = AppProtocol | None
type TMde = Literal["host", "ingress"] | None
TAll = tuple[TCpt, THpt, THip, TPrt, TApr, TNme, TMde, bool]

def create(args : TAll) -> Port:
    return create_obj_from_dict(Port, LABELS, *args)

def valid(port : TAll) -> bool:
    container_port, host_port, _, _, _, _, _, _ = port

    if (
        isinstance(container_port, tuple)
        and container_port[0] >= container_port[1]
    ):
        return False

    if (
        isinstance(host_port, tuple)
        and host_port[0] >= host_port[1]
    ):
        return False

    if (
        isinstance(container_port, tuple)
        and isinstance(host_port, tuple)
    ):
        s1, e1 = container_port
        s2, e2 = host_port

        if e1 - s1 != e2 - s2:
            return False

    if (
        isinstance(container_port, tuple)
        and isinstance(host_port, int)
    ):
        return False

    return True

container_port_values = [80, (8000, 8010), (8090, 8010), (12000, 13000)]

host_port_values = [8080, (9000, 9010), (9090, 9010), (14000, 15000)]

host_ip_values = [IPv4Address("192.168.0.1"), IPv6Address("::1"), None]

protocol_values = ["tcp", None]

name_values = ["mead", None]

app_protocol_values = [AppProtocol.http, None]

mode_values = ["host", None]

force_long_syntax_values = [False]

prod_all = list(product(
    container_port_values,
    host_port_values,
    host_ip_values,
    protocol_values,
    app_protocol_values,
    name_values,
    mode_values,
    force_long_syntax_values,
))

valid_ports = [t for t in prod_all if valid(t)] # type: ignore

invalid_ports = [t for t in prod_all if not valid(t)] # type: ignore

double_prod = random_choices(list(product(valid_ports, repeat = 2)), k = 100)

container_port_1 = 80
container_port_2 = (8000, 8010)
host_port_1 = 8080
host_port_2 = (9000, 9010)
host_ip_1 = IPv4Address("192.168.0.1")
host_ip_2 = IPv6Address("::1")
protocol = "tcp"
name = "mead"
app_protocol = AppProtocol.http
mode = "host"

full_ports = [
    ((container_port_1, None, None, None, None, None, None, False), "80"),
    ((container_port_1, None, None, None, None, None, None, True), {
        "target": "80",
    }),
    ((container_port_2, None, None, None, None, None, None, False), "8000-8010"),
    ((container_port_1, host_port_1, None, None, None, None, None, False), "8080:80"),
    ((container_port_2, host_port_2, None, None, None, None, None, False), "9000-9010:8000-8010"),
    ((container_port_1, host_port_2, None, None, None, None, None, False), "9000-9010:80"),
    ((container_port_2, None, host_ip_1, None, None, None, None, False), "192.168.0.1:8000-8010"),
    ((container_port_2, host_port_2, host_ip_1, None, None, None, None, False), "192.168.0.1:9000-9010:8000-8010"),
    ((container_port_2, None, host_ip_2, None, None, None, None, False), "::1:8000-8010"),
    ((container_port_2, None, None, protocol, None, None, None, False), "8000-8010/tcp"),
    ((container_port_1, host_port_1, host_ip_1, protocol, app_protocol, name, mode, False), {
        "name": "mead",
        "target": "80",
        "host_ip": "192.168.0.1",
        "published": "8080",
        "protocol": "tcp",
        "app_protocol": "http",
        "mode": "host",
    }),
]

## CREATION

@pytest.mark.parametrize("port", valid_ports)
def test_create(port : TAll):
    check_create_full(LABELS, port, create)


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("port", invalid_ports)
def test_create_fail(port : TAll):
    create(port)

## API

@pytest.mark.parametrize("port,expected", full_ports)
def test_full_port(port : TAll, expected : Configuration):
    assert create(port).get_full_port() == expected

## EQUALITY

@pytest.mark.parametrize("port1,port2", double_prod)
def test_equal(port1 : TAll, port2 : TAll):
    container_port1, _, _, _, _, _, _, _ = port1
    container_port2, _, _, _, _, _, _, _ = port2
    assert (create(port1) == create(port2)) == (container_port1 == container_port2)

## HASH

@pytest.mark.parametrize("port", valid_ports)
def test_hash(port : TAll):
    container_port, _, _, _, _, _, _, _ = port
    assert hash(create(port)) == hash(container_port)

## REPR

@pytest.mark.parametrize("port", valid_ports)
def test_repr(port : TAll):
    check_repr_full(LABELS, port, create)
