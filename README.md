# JourneyToPython

Petit projet d’apprentissage Python structuré “comme en production” : package en `src/`, CLI avec arguments, persistance CSV, tests, lint/format automatiques, et CI GitHub Actions.

## Objectifs

- Apprendre Python en construisant un projet réel (pas juste des scripts).
- Mettre en place de bonnes pratiques :
  - structure `src/`
  - exécution en module (`python -m ...`)
  - CLI (Command Line Interface) avec `argparse`
  - qualité de code (Ruff + pre-commit)
  - tests (pytest)
  - CI (GitHub Actions)

## Stack / outils

- Python (venv gérée par `uv`)
- `uv` : gestion de l’environnement + exécution (`uv run ...`)
- `argparse` : CLI standard Python
- CSV : stockage simple des données (fichier `people.csv`)
- `ruff` : lint + format
- `pytest` : tests
- GitHub Actions : CI

## Structure du projet

```text
JourneyToPython/
├─ src/
│  └─ journey_to_python/
│     ├─ __init__.py
│     ├─ __main__.py
│     ├─ app.py
│     ├─ cli.py
│     ├─ models/
│     │  └─ person.py
│     └─ storage/
│        └─ csv_store.py
├─ tests/
├─ pyproject.toml
├─ .pre-commit-config.yaml
└─ .github/workflows/ci.yml
