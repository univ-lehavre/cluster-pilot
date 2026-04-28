from k3scli.app import app, build_inspect_tables
from k3splan import AptState, CpuState, DiskState, MemoryState, ObservedState, SystemState
from typer.testing import CliRunner


def test_validate_command() -> None:
    result = CliRunner().invoke(app, ["validate", "examples/single-server.yaml"])

    assert result.exit_code == 0
    assert "OK" in result.stdout
    assert "prod-1" in result.stdout


def test_validate_command_with_inventory() -> None:
    result = CliRunner().invoke(
        app,
        [
            "validate",
            "examples/single-server.yaml",
            "--inventory",
            "examples/inventory.example.yaml",
        ],
    )

    assert result.exit_code == 0
    assert "OK" in result.stdout


def test_plan_command() -> None:
    result = CliRunner().invoke(app, ["plan", "examples/single-server.yaml"])

    assert result.exit_code == 0
    assert "Plan: prod-1" in result.stdout
    assert "Install k3s" in result.stdout


def test_inspect_requires_inventory_for_connection_ref() -> None:
    result = CliRunner().invoke(app, ["inspect", "examples/single-server.yaml"])

    assert result.exit_code != 0
    assert "manifest uses connectionRef but no inventory was provided" in result.output


def test_inspect_tables_are_grouped() -> None:
    observed = ObservedState(
        target="prod-1",
        sshAvailable=True,
        system=SystemState(
            os="Linux",
            distributionPrettyName="Ubuntu 24.04.4 LTS",
            architecture="x86_64",
            cpu=CpuState(cores=12, usagePercent=0.1),
            disk=DiskState(totalMiB=1000, usedPercent=1),
            memory=MemoryState(availableMiB=512),
            apt=AptState(available=True, upgradablePackages=0, systemUpToDate=True),
        ),
    )

    tables = build_inspect_tables(observed)

    assert [table.title for table in tables] == ["Connection", "System", "Resources", "APT", "k3s"]
