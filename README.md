# JourneyToPython

Petit projet d’apprentissage Python structuré **comme en production** :

- package en `src/`
- exécution en module
- CLI avec arguments
- persistance CSV
- tests automatisés
- lint / format
- CI GitHub Actions

---

## 🎯 Objectifs

- Apprendre Python en construisant un **projet réel** (pas juste des scripts).
- Mettre en place de bonnes pratiques :
  - structure `src/`
  - exécution en module (`python -m ...`)
  - CLI (Command Line Interface) avec `argparse`
  - qualité de code (Ruff + pre-commit)
  - tests (pytest)
  - CI (GitHub Actions)

---

## 🧰 Stack / outils

- **Python 3.12+**
- **uv** : gestion de l’environnement + exécution (`uv run ...`)
- **argparse** : CLI standard Python
- **CSV** : stockage simple des données (`people.csv`)
- **ruff** : lint + format
- **pytest** : tests
- **GitHub Actions** : CI

---

## Installation

### Prérequis

- Python 3.12+
- `uv` installé

### Setup du projet

uv venv --python 3.12
uv pip install -e .

## Utilisation

### Aide générale 

uv run journey-to-python --help

### Créer une personne

uv run journey-to-python person --name "John" --address "13 Main St"

### Avec email(s)

uv run journey-to-python person \
  --name "Alice" \
  --address "9 rue de la montagne en France" \
  --email test@email.fr \
  --email other@email.fr

### Lister des personnes

uv run journey-to-python list --csv people.csv

### Supprimer une personne par ID

uv run journey-to-python remove --id <ID> --csv people.csv

## Qualité de code

### Lint et format

uv run ruff check . --fix
uv run ruff format .

### Tests

uv run pytest -q

Les hooks pre-commit exécutent automatiquement Ruff avant chaque commit.

## CI

Une CI **GitHub Actions** est configurée pour exécuter :

- le lint
- le format
- les tests

À chaque **push** ou **pull request**.

---

## Notes

- Les emails sont stockés dans le CSV avec un séparateur `;`.
- Les dossiers générés (`.venv`, `*.egg-info`) sont ignorés par Git.