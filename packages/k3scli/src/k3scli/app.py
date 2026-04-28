from pathlib import Path

import typer
from k3splan import load_inventory, load_manifest, resolve_connection
from k3splan.planner import build_initial_plan
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Declarative k3s machine reconciler.")
console = Console()


@app.command()
def validate(manifest: Path, inventory: Path | None = None) -> None:
    """Validate a machine manifest."""
    desired = load_manifest(manifest)
    if inventory is not None:
        loaded_inventory = load_inventory(inventory)
        resolve_connection(desired, loaded_inventory)

    console.print(f"[green]OK[/] {desired.kind} {desired.metadata.name}")


@app.command()
def plan(manifest: Path) -> None:
    """Show the actions required to reach the desired state."""
    desired = load_manifest(manifest)
    generated_plan = build_initial_plan(desired)

    table = Table(title=f"Plan: {generated_plan.target}")
    table.add_column("#", justify="right")
    table.add_column("Action")
    table.add_column("Risk")
    table.add_column("Rollback")

    for index, action in enumerate(generated_plan.actions, start=1):
        table.add_row(str(index), action.description, action.risk, action.rollback)

    console.print(table)


@app.command()
def inspect(manifest: Path, inventory: Path | None = None) -> None:
    """Inspect the target machine without modifying it."""
    desired = load_manifest(manifest)
    if inventory is not None:
        loaded_inventory = load_inventory(inventory)
        connection = resolve_connection(desired, loaded_inventory)
        console.print(
            f"[yellow]Inspect is not implemented yet[/] for "
            f"{desired.metadata.name} via {connection.user}@{connection.host}"
        )
        return

    console.print(f"[yellow]Inspect is not implemented yet[/] for {desired.metadata.name}")
