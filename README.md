# k3s

Outil declaratif experimental pour inspecter, planifier et reconciler l'etat k3s
d'une machine distante.

## Developpement

Installer l'environnement :

```bash
uv sync --all-packages --dev
```

Lancer le CLI :

```bash
uv run k3sctl --help
uv run k3sctl validate examples/single-server.yaml
uv run k3sctl plan examples/single-server.yaml
```

Verifier le depot :

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy packages
uv run pytest
```

Installer les hooks Git :

```bash
uv run pre-commit install --hook-type pre-commit
uv run pre-commit install --hook-type pre-push
uv run pre-commit install --hook-type commit-msg
```

Lancer les hooks manuellement :

```bash
uv run pre-commit run --all-files
uv run pre-commit run --hook-stage pre-push --all-files
```

Gestion de version :

```bash
uv run cz bump --dry-run --yes
uv run cz bump
```

## Documentation

- [Architecture et phasage](docs/architecture.md)
- [Release](docs/release.md)
