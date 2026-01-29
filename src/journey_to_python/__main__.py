# src/journey_to_python/__main__.py

# Ce fichier est le **point d’entrée du package** quand on lance :
#   python -m journey_to_python
#
# Règle importante en Python :
# - si un dossier est un package (contient __init__.py)
# - et qu’il contient un fichier __main__.py
# alors Python exécutera automatiquement __main__.py
# lorsqu’on lance le package avec `-m`.

# On importe la fonction main() depuis app.py.
# app.py contient l’orchestration de l’application (CLI, parsing, délégation).
from .app import main

# Cette condition est une protection standard en Python.
# Elle garantit que le code à l’intérieur :
# - s’exécute UNIQUEMENT si ce fichier est le point d’entrée
# - ne s’exécute PAS si le module est importé ailleurs
#
# Ici, c’est surtout une bonne pratique de cohérence,
# même si __main__.py est rarement importé directement.
if __name__ == "__main__":
    # Appel du point d’entrée principal de l’application.
    # À partir d’ici :
    # - la CLI est construite
    # - les arguments sont parsés
    # - la logique métier est exécutée
    main()
