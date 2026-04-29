# Plan

Ce document suit le phasage du projet `k3sctl`.

## Table des matieres

- [Statuts](#statuts)
- [Etat actuel](#etat-actuel)
- [Phase 0 - Cadrage du socle](#phase-0---cadrage-du-socle)
- [Phase 1 - Manifeste et validation](#phase-1---manifeste-et-validation)
- [Phase 2 - Inspection lecture seule](#phase-2---inspection-lecture-seule)
- [Phase 3 - Planification](#phase-3---planification)
- [Phase 4 - Actions verifiables minimales](#phase-4---actions-verifiables-minimales)
- [Phase 5 - Runner transactionnel et journal](#phase-5---runner-transactionnel-et-journal)
- [Phase 6 - k3s present](#phase-6---k3s-present)
- [Phase 7 - k3s absent](#phase-7---k3s-absent)
- [Phase 8 - Health et drift](#phase-8---health-et-drift)
- [Phase 9 - Durcissement](#phase-9---durcissement)
- [Phase 10 - Agent Go et metriques continues](#phase-10---agent-go-et-metriques-continues)

## Statuts

- ✅ `done` : realise et verifie ;
- 🟡 `partial` : premiere version disponible, mais contrat incomplet ;
- ⬜ `todo` : non demarre.

## Etat actuel

```text
✅ Phase 0  Cadrage du socle
✅ Phase 1  Manifeste et validation
✅ Phase 2  Inspection lecture seule
✅ Phase 3  Planification
✅ Phase 4  Actions verifiables
✅ Phase 5  Runner et journal
✅ Phase 6  k3s present
✅ Phase 7  k3s absent
✅ Phase 8  Health et drift
🟡 Phase 9  Durcissement
🟡 Phase 10 Agent Go et metriques continues
```

## Phase 0 - Cadrage du socle

Statut : ✅ `done`

Objectif : obtenir un depot Python propre avec workspace `uv`.

Actions :

- ✅ creer le `pyproject.toml` racine
- ✅ configurer le workspace `uv`
- ✅ creer les paquets `k3splan`, `k3sremote`, `k3scli`
- ✅ configurer `pytest`, `ruff`, `mypy`
- ✅ exposer le script `k3sctl`
- ✅ ajouter `pre-commit` et les hooks Git
- ✅ ajouter Commitizen pour version, bump et changelog

Definition of done :

- ✅ `uv run k3sctl --help` fonctionne
- ✅ `uv run pytest` fonctionne
- ✅ `uv run ruff check .` fonctionne
- ✅ `uv run mypy packages` fonctionne
- ✅ `uv run pre-commit run --all-files` fonctionne
- ✅ `uv run pre-commit run --hook-stage pre-push --all-files` fonctionne

## Phase 1 - Manifeste et validation

Statut : ✅ `done`

Objectif : charger et valider un manifeste `Machine`.

Actions :

- ✅ definir les modeles Pydantic
- ✅ implementer le chargement YAML
- ✅ ajouter `examples/single-server.yaml`
- ✅ ajouter `examples/uninstall.yaml`
- ✅ ajouter `examples/inventory.example.yaml`
- ✅ ajouter la commande `k3sctl validate <manifest>`
- ✅ accepter `spec.connectionRef` pour eviter les connexions reelles dans les manifests publics
- ✅ ajouter `--inventory` pour valider la resolution de connexion
- ✅ ignorer `inventory.local.yaml` et `*.local.yaml`

Definition of done :

- ✅ un manifeste valide est accepte
- ✅ les erreurs de schema sont lisibles
- ✅ les tests couvrent les champs obligatoires et les valeurs invalides
- ✅ un manifeste avec `connectionRef` peut etre resolu via inventaire
- ✅ un manifeste sans source de connexion est refuse

Livrables :

- `packages/k3splan/src/k3splan/manifest.py`
- `examples/single-server.yaml`
- `examples/uninstall.yaml`
- `examples/inventory.example.yaml`
- `docs/manifest.md`

## Phase 2 - Inspection lecture seule

Statut : ✅ `done`

Objectif : observer une machine distante sans modifier son etat.

Actions :

- ✅ implementer une interface `RemoteExecutor`
- ✅ ajouter un adaptateur SSH
- ✅ collecter OS, distribution, version, architecture, systemd, k3s, disque, memoire
- ✅ collecter l'etat APT : disponibilite, fraicheur des listes et paquets upgradables
- ✅ collecter les paquets et sysctl declares dans le manifeste
- ✅ ajouter la commande `k3sctl inspect <manifest>`

Definition of done :

- ✅ l'inspection fonctionne sur une machine accessible en SSH
- ✅ l'etat observe est serialisable en JSON
- ✅ les tests unitaires utilisent un faux executor

Regle APT :

- ✅ `apt system up to date` vaut `yes` seulement si les listes APT sont recentes et si aucun paquet n'est upgradable

Ameliorations futures :

- ⬜ ajouter une sortie JSON pour automatisation

## Phase 3 - Planification

Statut : ✅ `done`

Objectif : produire un plan d'actions sans appliquer.

Actions :

- ✅ definir les classes `ObservedState`, `Plan` et `ActionSpec`
- ✅ implementer le diff `desired + observed -> plan`
- ✅ ajouter la commande `k3sctl plan <manifest>`
- ✅ afficher le plan avec `rich`

Definition of done :

- ✅ une machine sans k3s produit un plan d'installation avec etat observe
- ✅ une machine conforme produit un plan reduit aux actions necessaires
- ✅ une machine avec derive de version produit une action d'upgrade

Livrables :

- `packages/k3splan/src/k3splan/planner.py`
- `packages/k3splan/src/k3splan/observed.py`

## Phase 4 - Actions verifiables minimales

Statut : ✅ `done`

Objectif : executer des actions simples et les verifier.

Actions :

- ✅ implementer `EnsurePackagePresent`
- ✅ implementer `WriteRemoteFile` avec backup
- ✅ implementer `SetSysctlValue`
- ✅ definir `precheck`, `snapshot`, `apply`, `verify`, `rollback`

Definition of done :

- ✅ chaque action peut etre testee avec un executor fake
- ✅ chaque action expose son mode de rollback
- ✅ une verification echouee est detectee

Livrables :

- `packages/k3splan/src/k3splan/actions.py`
- `packages/k3sremote/src/k3sremote/actions.py`

## Phase 5 - Runner transactionnel et journal

Statut : ✅ `done`

Objectif : executer un plan avec journalisation et rollback.

Actions :

- ✅ implementer le `Runner`
- ✅ ecrire un journal local par `run_id`
- ✅ enregistrer snapshots, statuts et erreurs
- ✅ executer le rollback en ordre inverse
- ✅ ajouter `k3sctl apply <manifest>`

Definition of done :

- ✅ une action echouee stoppe l'execution
- ✅ les actions deja appliquees sont rollbackees si possible
- ✅ `k3sctl journal list` liste les executions
- ⬜ `k3sctl rollback --run-id <run-id>` fonctionne pour les actions rollbackables

Livrables :

- `packages/k3splan/src/k3splan/runner.py`
- `packages/k3splan/src/k3splan/journal.py`
- `packages/k3sremote/src/k3sremote/builder.py`

## Phase 6 - k3s present

Statut : ✅ `done`

Objectif : installer et demarrer k3s declarativement.

Actions :

- ✅ implementer `InstallK3s`
- ✅ implementer `WriteK3sConfig` (via `WriteRemoteFile`)
- ✅ implementer `SystemdServiceEnable`
- ✅ implementer `SystemdServiceStart`
- ✅ implementer `WaitK3sNodeReady`
- ✅ implementer `FetchKubeconfig`

Definition of done :

- ✅ `k3sctl plan` annonce les actions d'installation
- ✅ `k3sctl apply` execute le plan complet via le runner transactionnel
- ⬜ `k3sctl verify` confirme service running, version attendue et node ready (Phase 8)

Livrables :

- `packages/k3sremote/src/k3sremote/actions.py` (InstallK3s, SystemdServiceEnable, SystemdServiceStart, WaitK3sNodeReady, FetchKubeconfig)
- `packages/k3sremote/src/k3sremote/builder.py` (actions k3s cablees)

## Phase 7 - k3s absent

Statut : ✅ `done`

Objectif : desinstaller k3s proprement.

Actions :

- ✅ implementer `UninstallK3s`
- ✅ gerer `removeData` (script complet ou suppression selective)
- ✅ gerer `removeKubeconfig` (suppression du kubeconfig local)
- ✅ verifier absence du binaire k3s apres desinstallation

Definition of done :

- ✅ `state: absent` produit un plan de desinstallation
- ⬜ la desinstallation est bloquee ou confirmee si elle est destructive (Phase 9)
- ✅ la verification confirme l'absence attendue

Livrables :

- `packages/k3sremote/src/k3sremote/actions.py` (UninstallK3s)
- `packages/k3sremote/src/k3sremote/builder.py` (k3s.uninstall cable)

## Phase 8 - Health et drift

Statut : ✅ `done`

Objectif : rendre l'outil utile au quotidien.

Actions :

- ✅ ajouter `k3sctl doctor <manifest>`
- ✅ ajouter `k3sctl drift <manifest>`
- ✅ structurer les checks de sante
- ✅ afficher un verdict clair : `healthy`, `degraded`, `unhealthy`

Definition of done :

- ✅ le rapport distingue sante systeme, sante k3s et derive declarative
- ✅ les seuils du manifeste sont appliques (diskFreePercent, memoryFreeMiB)
- ✅ drift affiche les actions necessaires et retourne exit code 1 si derive detectee

Livrables :

- `packages/k3splan/src/k3splan/health.py`

## Phase 9 - Durcissement

Statut : 🟡 `partial`

Objectif : rendre le projet robuste avant usage reel.

Actions :

- ⬜ ajouter tests d'integration sur VM ou container systemd si possible
- ✅ documenter les limites de rollback
- ✅ documenter les risques d'upgrade k3s
- ✅ ajouter mode `--dry-run` sur `k3sctl apply`
- ✅ ajouter confirmations pour actions a risque eleve
- ⬜ stabiliser le schema `v1alpha1`
- ✅ documenter la separation manifeste public / inventaire prive
- ✅ ajouter hooks qualite locaux
- ✅ ajouter workflow de release local

Definition of done :

- ✅ la documentation couvre installation, desinstallation, rollback et limites
- ✅ les commandes critiques ont des tests
- ✅ les erreurs CLI sont comprehensibles et actionnables

## Phase 10 - Agent Go et metriques continues

Statut : 🟡 `partial`

Objectif : fournir un canal durable pour streamer des metriques systeme sans
dependre d'une commande SSH longue duree.

Actions :

- ✅ creer `agents/k3sagent` avec un module Go dedie
- ✅ creer `proto/k3smetrics.proto` comme contrat source
- ⬜ generer les stubs Go et Python depuis le contrat Protobuf
- ⬜ implementer `StreamCpu` en gRPC dans l'agent Go
- ⬜ faire ecouter l'agent sur `127.0.0.1` par defaut
- ⬜ ajouter un client Python dans `k3sremote`
- ⬜ documenter le tunnel SSH vers l'agent
- ✅ ajouter `go test ./...` et `go build` aux verifications du depot

Definition of done :

- ✅ un agent Go peut etre compile en binaire autonome
- ⬜ `k3sctl` peut consommer le stream CPU via gRPC
- ⬜ le flux fonctionne quand le seul acces reseau est SSH
- ⬜ les contrats Protobuf sont versionnes et partages par Go et Python
