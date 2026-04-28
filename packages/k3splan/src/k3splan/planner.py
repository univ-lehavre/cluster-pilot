from dataclasses import dataclass

from k3splan.manifest import DesiredState


@dataclass(frozen=True)
class PlannedAction:
    id: str
    description: str
    risk: str = "low"
    rollback: str = "none"


@dataclass(frozen=True)
class Plan:
    target: str
    actions: list[PlannedAction]

    @property
    def empty(self) -> bool:
        return not self.actions


def build_initial_plan(desired: DesiredState) -> Plan:
    actions: list[PlannedAction] = []

    for package in desired.spec.system.packages.present:
        actions.append(
            PlannedAction(
                id=f"package.present.{package}",
                description=f"Ensure package {package} is present",
                rollback="none",
            )
        )

    for key, value in desired.spec.system.sysctl.items():
        actions.append(
            PlannedAction(
                id=f"sysctl.{key}",
                description=f"Set sysctl {key} = {value}",
                rollback="reversible",
            )
        )

    if desired.spec.k3s.state == "present":
        version = desired.spec.k3s.version or desired.spec.k3s.install.channel
        actions.extend(
            [
                PlannedAction(
                    id="k3s.config.write",
                    description="Write /etc/rancher/k3s/config.yaml",
                    rollback="reversible",
                ),
                PlannedAction(
                    id="k3s.install",
                    description=f"Install k3s {version}",
                    risk="medium",
                    rollback="compensating",
                ),
                PlannedAction(
                    id="systemd.k3s.enable",
                    description="Enable k3s service",
                    rollback="reversible",
                ),
                PlannedAction(
                    id="systemd.k3s.start",
                    description="Start k3s service",
                    rollback="reversible",
                ),
                PlannedAction(
                    id="k3s.node.ready",
                    description="Wait for node Ready",
                    rollback="none",
                ),
            ]
        )
    else:
        actions.append(
            PlannedAction(
                id="k3s.uninstall",
                description="Uninstall k3s",
                risk="high" if desired.spec.k3s.uninstall.removeData else "medium",
                rollback="compensating",
            )
        )

    return Plan(target=desired.metadata.name, actions=actions)
