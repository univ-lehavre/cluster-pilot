from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from ruamel.yaml import YAML


class Metadata(BaseModel):
    name: str
    labels: dict[str, str] = Field(default_factory=dict)


class Connection(BaseModel):
    type: Literal["ssh"]
    host: str
    user: str
    port: int = 22


class Packages(BaseModel):
    present: list[str] = Field(default_factory=list)


class System(BaseModel):
    packages: Packages = Field(default_factory=Packages)
    sysctl: dict[str, str] = Field(default_factory=dict)


class K3sInstall(BaseModel):
    channel: str = "stable"
    method: Literal["official-script"] = "official-script"


class K3sService(BaseModel):
    enabled: bool = True
    running: bool = True


class K3sUninstall(BaseModel):
    removeData: bool = False
    removeKubeconfig: bool = False


class K3s(BaseModel):
    state: Literal["present", "absent"]
    role: Literal["server", "agent"] | None = None
    version: str | None = None
    install: K3sInstall = Field(default_factory=K3sInstall)
    config: dict[str, object] = Field(default_factory=dict)
    service: K3sService = Field(default_factory=K3sService)
    uninstall: K3sUninstall = Field(default_factory=K3sUninstall)


class Health(BaseModel):
    require: list[str] = Field(default_factory=list)
    thresholds: dict[str, int] = Field(default_factory=dict)


class PlanOptions(BaseModel):
    showDiff: bool = True
    includeNoop: bool = False


class VerifyOptions(BaseModel):
    afterEachAction: bool = True
    timeoutSeconds: int = 120


class RollbackOptions(BaseModel):
    enabled: bool = True
    on: list[str] = Field(default_factory=lambda: ["applyFailure", "verifyFailure"])
    requireConfirmFor: list[str] = Field(default_factory=list)
    strategy: str = "reverse-applied-actions"


class JournalOptions(BaseModel):
    location: Literal["local"] = "local"
    path: str = ".k3sctl/runs"
    keep: int = 20


class Execution(BaseModel):
    mode: Literal["transactional"] = "transactional"
    plan: PlanOptions = Field(default_factory=PlanOptions)
    verify: VerifyOptions = Field(default_factory=VerifyOptions)
    rollback: RollbackOptions = Field(default_factory=RollbackOptions)
    journal: JournalOptions = Field(default_factory=JournalOptions)


class Spec(BaseModel):
    connection: Connection
    system: System = Field(default_factory=System)
    k3s: K3s
    health: Health = Field(default_factory=Health)
    execution: Execution = Field(default_factory=Execution)


class DesiredState(BaseModel):
    apiVersion: Literal["k3sctl.dev/v1alpha1"]
    kind: Literal["Machine"]
    metadata: Metadata
    spec: Spec


def load_manifest(path: Path) -> DesiredState:
    yaml = YAML(typ="safe")
    raw = yaml.load(path.read_text(encoding="utf-8"))
    return DesiredState.model_validate(raw)
