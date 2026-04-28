# Release

Le depot utilise une version unique synchronisee pour tous les paquets du
monorepo :

- `k3s-workspace`
- `k3splan`
- `k3sremote`
- `k3scli`

Les versions sont mises a jour ensemble par Commitizen.

## Commits

Les messages de commit suivent Conventional Commits :

```text
feat: add manifest validation
fix: handle missing k3s binary
docs: document rollback guarantees
test: add planner tests
refactor: split action model
chore: update dependencies
```

Effet sur la version :

```text
fix:      patch
feat:     minor
BREAKING: major
```

Tant que le projet reste en `0.x`, `major_version_zero = true` limite les bumps
majeurs automatiques.

## Bump

Verifier le depot :

```bash
uv run pre-commit run --all-files
uv run pre-commit run --hook-stage pre-push --all-files
```

Previsualiser le prochain bump :

```bash
uv run cz bump --dry-run --yes
```

Creer la release :

```bash
uv run cz bump
git push
git push --tags
```

Commitizen met a jour :

- les versions des `pyproject.toml` ;
- `CHANGELOG.md` ;
- le tag Git `vX.Y.Z`.
