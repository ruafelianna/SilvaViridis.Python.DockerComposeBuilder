import pytest

from ipaddress import IPv4Address, IPv6Address
from pydantic import ValidationError
from typing import Literal

from SilvaViridis.Python.DockerComposeBuilder.Common import AppProtocol
from SilvaViridis.Python.DockerComposeBuilder.Services import Port, TPort, TPortRange

ports_single = [80]

ports_paired = [(8000, 8010)]

container_ports_single = ports_single

container_ports_paired = ports_paired

host_ports = [None] + ports_single + ports_paired

host_ips = [None, IPv4Address("192.168.0.1"), IPv6Address("::1")]

protocols = [None, "tcp", "udp"]

names = [None, "apple"]

app_protocols = [None, AppProtocol.http, AppProtocol.https]

modes = [None, "host", "ingress"]

incorrect_range = [(8090, 8010)]

long_range = [(12000, 13000)]

## CREATION

@pytest.mark.parametrize("container_port", container_ports_single)
@pytest.mark.parametrize("host_port", host_ports)
@pytest.mark.parametrize("host_ip", host_ips)
@pytest.mark.parametrize("protocol", protocols)
def test_create_short(
    container_port : TPort | TPortRange, host_port : TPort | TPortRange | None,
    host_ip : IPv4Address | IPv6Address | None, protocol : Literal["tcp", "udp"] | None,
):
    port = Port(
        container_port = container_port,
        host_port = host_port,
        host_ip = host_ip,
        protocol = protocol,
    )
    assert (
        port.container_port,
        port.host_port,
        port.host_ip,
        port.protocol,
        port.name,
        port.app_protocol,
        port.mode,
        port.force_long_syntax,
    ) == (
        container_port,
        host_port,
        host_ip,
        protocol,
        None,
        None,
        None,
        False,
    )


@pytest.mark.parametrize("container_port", container_ports_paired)
def test_create_forced(container_port : TPort | TPortRange):
    port = Port(
        container_port = container_port,
        force_long_syntax = True,
    )
    assert (
        port.container_port,
        port.host_port,
        port.host_ip,
        port.protocol,
        port.name,
        port.app_protocol,
        port.mode,
        port.force_long_syntax,
    ) == (
        container_port,
        None,
        None,
        None,
        None,
        None,
        None,
        True,
    )


@pytest.mark.parametrize("container_port", container_ports_single)
@pytest.mark.parametrize("host_port", host_ports)
@pytest.mark.parametrize("host_ip", host_ips)
@pytest.mark.parametrize("protocol", protocols)
@pytest.mark.parametrize("name", names)
@pytest.mark.parametrize("app_protocol", app_protocols)
@pytest.mark.parametrize("mode", modes)
def test_create_full(
    container_port : TPort | TPortRange, host_port : TPort | TPortRange | None,
    host_ip : IPv4Address | IPv6Address | None, protocol : Literal["tcp", "udp"] | None,
    name : str | None, app_protocol : AppProtocol | None, mode : Literal["host", "ingress"] | None,
):
    port = Port(
        container_port = container_port,
        host_port = host_port,
        host_ip = host_ip,
        protocol = protocol,
        name = name,
        app_protocol = app_protocol,
        mode = mode,
    )
    assert (
        port.container_port,
        port.host_port,
        port.host_ip,
        port.protocol,
        port.name,
        port.app_protocol,
        port.mode,
        port.force_long_syntax,
    ) == (
        container_port,
        host_port,
        host_ip,
        protocol,
        name,
        app_protocol,
        mode,
        False,
    )


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("container_port", incorrect_range)
def test_create_fail_container_range(container_port : TPort | TPortRange):
    Port(
        container_port = container_port,
    )


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("container_port", container_ports_paired)
@pytest.mark.parametrize("host_port", incorrect_range)
def test_create_fail_host_range(container_port : TPort | TPortRange, host_port : TPort | TPortRange | None):
    Port(
        container_port = container_port,
        host_port = host_port,
    )


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("container_port", long_range)
@pytest.mark.parametrize("host_port", ports_paired)
def test_create_fail_long_container(container_port : TPort | TPortRange, host_port : TPort | TPortRange | None):
    Port(
        container_port = container_port,
        host_port = host_port,
    )


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("container_port", container_ports_paired)
@pytest.mark.parametrize("host_port", long_range)
def test_create_fail_long_host(container_port : TPort | TPortRange, host_port : TPort | TPortRange | None):
    Port(
        container_port = container_port,
        host_port = host_port,
    )


@pytest.mark.xfail(raises = ValidationError)
@pytest.mark.parametrize("container_port", container_ports_paired)
@pytest.mark.parametrize("host_port", ports_single)
def test_create_fail_mapping(container_port : TPort | TPortRange, host_port : TPort | TPortRange | None):
    Port(
        container_port = container_port,
        host_port = host_port,
    )

## API

@pytest.mark.parametrize("container_port", container_ports_single)
@pytest.mark.parametrize("host_port", host_ports)
@pytest.mark.parametrize("host_ip", host_ips)
@pytest.mark.parametrize("protocol", protocols)
def test_full_port_short(
    container_port : TPort | TPortRange, host_port : TPort | TPortRange | None,
    host_ip : IPv4Address | IPv6Address | None, protocol : Literal["tcp", "udp"] | None,
):
    port = Port(
        container_port = container_port,
        host_port = host_port,
        host_ip = host_ip,
        protocol = protocol,
    )
    hip = "" if host_ip is None else f"{host_ip}:"
    hport = "" if host_port is None else str(host_port) if isinstance(host_port, int) else f"{host_port[0]}-{host_port[1]}"
    hport = "" if hport == "" else f"{hport}:"
    cport = str(container_port) if isinstance(container_port, int) else f"{container_port[0]}-{container_port[1]}"
    prot = "" if protocol is None else f"/{protocol}"
    assert port.get_full_port() == f"{hip}{hport}{cport}{prot}"


@pytest.mark.parametrize("container_port", container_ports_single)
@pytest.mark.parametrize("host_port", host_ports)
@pytest.mark.parametrize("host_ip", host_ips)
@pytest.mark.parametrize("protocol", protocols)
@pytest.mark.parametrize("name", names)
@pytest.mark.parametrize("app_protocol", app_protocols)
@pytest.mark.parametrize("mode", modes)
def test_full_port_long(
    container_port : TPort | TPortRange, host_port : TPort | TPortRange | None,
    host_ip : IPv4Address | IPv6Address | None, protocol : Literal["tcp", "udp"] | None,
    name : str | None, app_protocol : AppProtocol | None, mode : Literal["host", "ingress"] | None,
):
    port = Port(
        container_port = container_port,
        host_port = host_port,
        host_ip = host_ip,
        protocol = protocol,
        name = name,
        app_protocol = app_protocol,
        mode = mode,
        force_long_syntax = True,
    )
    expected = {
        "target": str(container_port) if isinstance(container_port, int) else f"{container_port[0]}-{container_port[1]}",
        "published" : None if host_port is None else str(host_port) if isinstance(host_port, int) else f"{host_port[0]}-{host_port[1]}",
        "host_ip" : None if host_ip is None else str(host_ip),
        "name" : name,
        "protocol" : protocol,
        "app_protocol" : None if app_protocol is None else app_protocol.name,
        "mode" : mode,
    }
    assert port.get_full_port() == {k: v for k, v in expected.items() if v is not None}

## EQUALITY

@pytest.mark.parametrize("container_port1", container_ports_single)
@pytest.mark.parametrize("host_port1", host_ports)
@pytest.mark.parametrize("host_ip1", host_ips)
@pytest.mark.parametrize("protocol1", protocols)
@pytest.mark.parametrize("container_port2", container_ports_single)
@pytest.mark.parametrize("host_port2", host_ports)
@pytest.mark.parametrize("host_ip2", host_ips)
@pytest.mark.parametrize("protocol2", protocols)
def test_equal(
    container_port1 : TPort | TPortRange, host_port1 : TPort | TPortRange | None,
    host_ip1 : IPv4Address | IPv6Address | None, protocol1 : Literal["tcp", "udp"] | None,
    container_port2 : TPort | TPortRange, host_port2 : TPort | TPortRange | None,
    host_ip2 : IPv4Address | IPv6Address | None, protocol2 : Literal["tcp", "udp"] | None,
):
    port1 = Port(
        container_port = container_port1,
        host_port = host_port1,
        host_ip = host_ip1,
        protocol = protocol1,
    )
    port2 = Port(
        container_port = container_port2,
        host_port = host_port2,
        host_ip = host_ip2,
        protocol = protocol2,
    )
    assert (port1 == port2) == (container_port1 == container_port2)

## HASH

@pytest.mark.parametrize("container_port", container_ports_single)
@pytest.mark.parametrize("host_port", host_ports)
@pytest.mark.parametrize("host_ip", host_ips)
@pytest.mark.parametrize("protocol", protocols)
def test_hash(
    container_port : TPort | TPortRange, host_port : TPort | TPortRange | None,
    host_ip : IPv4Address | IPv6Address | None, protocol : Literal["tcp", "udp"] | None,
):
    port = Port(
        container_port = container_port,
        host_port = host_port,
        host_ip = host_ip,
        protocol = protocol,
    )
    assert hash(port) == hash(container_port)

## REPR

@pytest.mark.parametrize("container_port", container_ports_single)
@pytest.mark.parametrize("host_port", host_ports)
@pytest.mark.parametrize("host_ip", host_ips)
@pytest.mark.parametrize("protocol", protocols)
def test_repr(
    container_port : TPort | TPortRange, host_port : TPort | TPortRange | None,
    host_ip : IPv4Address | IPv6Address | None, protocol : Literal["tcp", "udp"] | None,
):
    port = Port(
        container_port = container_port,
        host_port = host_port,
        host_ip = host_ip,
        protocol = protocol,
    )
    assert repr(port) == f"{{'container_port': {repr(container_port)}, 'host_port': {repr(host_port)}, 'host_ip': {repr(host_ip)}, 'protocol': {repr(protocol)}, 'app_protocol': None, 'name': None, 'mode': None, 'force_long_syntax': False}}"
