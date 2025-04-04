import pytest

from ipaddress import IPv4Address, IPv6Address
from itertools import product
from pydantic import ValidationError
from random import choices as random_choices
from typing import Literal

from SilvaViridis.Python.DockerComposeBuilder.Common import AppProtocol, Configuration
from SilvaViridis.Python.DockerComposeBuilder.Services import Port, TPort, TPortRange

type TCpt = TPort | TPortRange
type THpt = TPort | TPortRange | None
type THip = IPv4Address | IPv6Address | None
type TPrt = Literal["tcp", "udp"] | None
type TNme = str | None
type TApr = AppProtocol | None
type TMde = Literal["host", "ingress"] | None
TAll = tuple[TCpt, THpt, THip, TPrt, TNme, TApr, TMde, bool]

container_ports = [80, (8000, 8010), (8090, 8010), (12000, 13000)]

host_ports = [8080, (9000, 9010), (9090, 9010), (14000, 15000)]

host_ips = [IPv4Address("192.168.0.1"), IPv6Address("::1"), None]

protocols = ["tcp", None]

names = ["mead", None]

app_protocols = [AppProtocol.http, None]

modes = ["host", None]

force_long_syntax_options = [False]

prod_all = list(product(container_ports, host_ports, host_ips, protocols, names, app_protocols, modes, force_long_syntax_options))

cp0 = container_ports[0]
cp1 : TPortRange = container_ports[1] # type: ignore
hp0 = host_ports[0]
hp1 : TPortRange = host_ports[1] # type: ignore
hi0 = host_ips[0]
hi1 = host_ips[1]
pr0 = protocols[0]
nm0 = names[0]
ap0 : AppProtocol = app_protocols[0] # type: ignore
md0 = modes[0]

full_ports = [
    ((cp0, None, None, None, None, None, None, False), f"{cp0}"),
    ((cp1, None, None, None, None, None, None, False), f"{cp1[0]}-{cp1[1]}"),
    ((cp0, hp0, None, None, None, None, None, False), f"{hp0}:{cp0}"),
    ((cp1, hp1, None, None, None, None, None, False), f"{hp1[0]}-{hp1[1]}:{cp1[0]}-{cp1[1]}"),
    ((cp0, hp1, None, None, None, None, None, False), f"{hp1[0]}-{hp1[1]}:{cp0}"),
    ((cp1, None, hi0, None, None, None, None, False), f"{hi0}:{cp1[0]}-{cp1[1]}"),
    ((cp1, hp1, hi0, None, None, None, None, False), f"{hi0}:{hp1[0]}-{hp1[1]}:{cp1[0]}-{cp1[1]}"),
    ((cp1, None, hi1, None, None, None, None, False), f"{hi1}:{cp1[0]}-{cp1[1]}"),
    ((cp1, None, None, pr0, None, None, None, False), f"{cp1[0]}-{cp1[1]}/{pr0}"),
    ((cp0, hp0, hi0, pr0, nm0, ap0, md0, False), {
        "name": nm0,
        "target": f"{cp0}",
        "host_ip": f"{hi0}",
        "published": f"{hp0}",
        "protocol": pr0,
        "app_protocol": ap0.name,
        "mode": md0,
    }),
]

def create(container_port : TCpt, host_port : THpt, host_ip : THip, protocol : TPrt, name : TNme, app_protocol : TApr, mode : TMde, force_long_syntax : bool):
    return Port(
        container_port = container_port,
        host_port = host_port,
        host_ip = host_ip,
        protocol = protocol,
        name = name,
        app_protocol = app_protocol,
        mode = mode,
        force_long_syntax = force_long_syntax,
    )

def valid(container_port : TCpt, host_port : THpt, host_ip : THip, protocol : TPrt, name : TNme, app_protocol : TApr, mode : TMde, force_long_syntax : bool):
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

valid_ports = [t for t in prod_all if valid(*t)] # type: ignore

invalid_ports = [t for t in prod_all if not valid(*t)] # type: ignore

double_prod = random_choices(list(product(valid_ports, repeat = 2)), k = 100)

## CREATION

@pytest.mark.parametrize("port", valid_ports)
def test_create(port : TAll):
    port_obj = create(*port)
    assert (
        port_obj.container_port,
        port_obj.host_port,
        port_obj.host_ip,
        port_obj.protocol,
        port_obj.name,
        port_obj.app_protocol,
        port_obj.mode,
        port_obj.force_long_syntax,
    ) == port


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("port", invalid_ports)
def test_create_fail(port : TAll):
    create(*port)

## API

@pytest.mark.parametrize("port,expected", full_ports)
def test_full_port(port : TAll, expected : Configuration):
    assert create(*port).get_full_port() == expected

## EQUALITY

@pytest.mark.parametrize("port1,port2", double_prod)
def test_equal(port1 : TAll, port2 : TAll):
    container_port1, _, _, _, _, _, _, _ = port1
    container_port2, _, _, _, _, _, _, _ = port2
    assert (create(*port1) == create(*port2)) == (container_port1 == container_port2)

## HASH

@pytest.mark.parametrize("port", valid_ports)
def test_hash(port : TAll):
    container_port, _, _, _, _, _, _, _ = port
    assert hash(create(*port)) == hash(container_port)

## REPR

@pytest.mark.parametrize("port", valid_ports)
def test_repr(port : TAll):
    container_port, host_port, host_ip, protocol, name, app_protocol, mode, force_long_syntax = port
    assert repr(create(*port)) == f"{{'container_port': {repr(container_port)}, 'host_port': {repr(host_port)}, 'host_ip': {repr(host_ip)}, 'protocol': {repr(protocol)}, 'app_protocol': {repr(app_protocol)}, 'name': {repr(name)}, 'mode': {repr(mode)}, 'force_long_syntax': {repr(force_long_syntax)}}}"
