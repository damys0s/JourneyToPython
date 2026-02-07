# JourneyToPython

`JourneyToPython` est une application CLI Python de gestion de personnes, construite comme un mini projet de production.

Le projet sert à la fois de terrain de progression Python et de démonstration de bonnes pratiques d'ingénierie logicielle: architecture en couches, contrat de persistance, tests automatisés, qualité de code et CI.

## Objectifs

- Consolider les fondamentaux Python sur un projet réel.
- Travailler une architecture maintenable (`domain` / `services` / `repositories` / `infrastructure`).
- Implémenter plusieurs backends de persistance sans changer la logique métier.
- Renforcer la qualité avec tests, linting et automatisation CI.

## Fonctionnalités

- `person`: créer une personne
- `list`: lister les personnes
- `get`: récupérer une personne par ID
- `update`: mise à jour partielle d'une personne
- `remove`: supprimer une personne par ID
- `find`: recherche multi-critères (`name`, `address`, `active/inactive`, `email`)

## Backends supportés

- CSV (`people.csv`)
- SQLite (`people.db`)

Sélection via `--backend csv|sqlite` sur les commandes CLI.

## Architecture

```text
CLI (argparse)
  -> services (règles métier, validations)
    -> PeopleRepository (contrat)
      -> CsvPeopleRepository | SQLitePeopleRepository (implémentations)
```

Structure principale:

```text
src/journey_to_python/
  app.py
  cli.py
  domain.py
  services.py
  repositories.py
  infrastructure/
    csv_repository.py
    sqlite_repository.py
tests/
```

## Stack

- Python 3.12+
- `uv` (environnement + exécution)
- `argparse` (CLI)
- `pytest` (tests)
- `ruff` (lint + format)
- GitHub Actions (CI)

## Installation

Prérequis:

- Python 3.12+
- `uv`

Setup:

```bash
uv venv --python 3.12
uv sync --dev
```

## Utilisation

Aide:

```bash
uv run journey-to-python --help
```

### Exemples avec backend CSV

Créer:

```bash
uv run journey-to-python person --name "Alice" --address "Rue 1" --email "alice@example.com" --backend csv --csv people.csv
```

Lister:

```bash
uv run journey-to-python list --backend csv --csv people.csv
```

Récupérer par ID:

```bash
uv run journey-to-python get --id ABCDEFGHIJKL --backend csv --csv people.csv
```

Mettre à jour:

```bash
uv run journey-to-python update --id ABCDEFGHIJKL --address "Nouvelle adresse" --backend csv --csv people.csv
```

Supprimer:

```bash
uv run journey-to-python remove --id ABCDEFGHIJKL --backend csv --csv people.csv
```

Rechercher:

```bash
uv run journey-to-python find --name "alice" --active --backend csv --csv people.csv
```

### Exemples avec backend SQLite

Créer:

```bash
uv run journey-to-python person --name "Bob" --address "Rue 2" --email "bob@example.com" --backend sqlite --sqlite people.db
```

Lister:

```bash
uv run journey-to-python list --backend sqlite --sqlite people.db
```

Rechercher:

```bash
uv run journey-to-python find --email "bob@example.com" --backend sqlite --sqlite people.db
```

## Qualité de code

Lint:

```bash
uv run ruff check .
```

Format:

```bash
uv run ruff format .
```

Tests:

```bash
uv run pytest -q
```

## CI

La CI GitHub Actions exécute les checks de qualité (lint/format) et les tests sur push / pull request.

## État actuel

- Couverture de tests active sur services, repositories (CSV/SQLite) et smoke CLI
- Contrat de persistance unifié (`PeopleRepository`)
- Implémentations CSV et SQLite validées

## Roadmap (prochaine étape)

- enrichir les validations métier (données d'entrée)
- améliorer la recherche (`find`) pour gérer plusieurs emails en critère
- ajouter des tests d'intégration CLI supplémentaires
- préparer une exposition API (FastAPI) en réutilisant la couche services
