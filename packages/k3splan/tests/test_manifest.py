from pathlib import Path

from k3splan import load_manifest
from k3splan.planner import build_initial_plan


def test_load_manifest() -> None:
    desired = load_manifest(Path("examples/single-server.yaml"))

    assert desired.metadata.name == "prod-1"
    assert desired.spec.connection.host == "10.0.0.12"
    assert desired.spec.k3s.state == "present"


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
