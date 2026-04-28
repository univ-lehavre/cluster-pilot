from pathlib import Path

from k3splan import load_inventory, load_manifest, resolve_connection
from k3splan.planner import build_initial_plan
from pydantic import ValidationError


def test_load_manifest() -> None:
    desired = load_manifest(Path("examples/single-server.yaml"))

    assert desired.metadata.name == "prod-1"
    assert desired.spec.connectionRef == "prod-1"
    assert desired.spec.k3s.state == "present"


def test_resolve_connection_from_inventory() -> None:
    desired = load_manifest(Path("examples/single-server.yaml"))
    inventory = load_inventory(Path("examples/inventory.example.yaml"))

    connection = resolve_connection(desired, inventory)

    assert connection.host == "192.0.2.10"
    assert connection.user == "root"


def test_manifest_requires_one_connection_source() -> None:
    try:
        load_manifest(Path("examples/invalid-missing-connection.yaml"))
    except ValidationError as exc:
        assert "spec must define exactly one of connection or connectionRef" in str(exc)
    else:
        raise AssertionError("manifest should be invalid without a connection source")


def test_build_initial_plan() -> None:
    desired = load_manifest(Path("examples/single-server.yaml"))
    plan = build_initial_plan(desired)

    assert plan.target == "prod-1"
    assert [action.id for action in plan.actions] == [
        "package.present.curl",
        "package.present.iptables",
        "package.present.ca-certificates",
        "sysctl.net.ipv4.ip_forward",
        "sysctl.net.bridge.bridge-nf-call-iptables",
        "k3s.config.write",
        "k3s.install",
        "systemd.k3s.enable",
        "systemd.k3s.start",
        "k3s.node.ready",
    ]
