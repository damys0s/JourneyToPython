# src/journey_to_python/__init__.py

# Ce fichier indique à Python que ce dossier est un **package Python**.
# Sans __init__.py :
# - Python ne traiterait pas ce dossier comme un package "classique"
# - les imports comme `import journey_to_python` ou
#   `from journey_to_python.models import Person`
#   ne fonctionneraient pas correctement (ou pas du tout selon le contexte)
#
# Historiquement, __init__.py était obligatoire pour créer un package.
# Aujourd’hui (Python ≥ 3.3), il est parfois optionnel,
# mais dans les projets professionnels, on le garde toujours :
# - clarté
# - compatibilité
# - contrôle explicite du package

# Ce fichier est exécuté automatiquement UNE SEULE FOIS :
# - au premier `import journey_to_python`
# - ou lors du lancement `python -m journey_to_python`
#
# ⚠️ Règle importante :
# __init__.py ne doit PAS contenir de logique lourde.
# Pas de print(), pas d’accès réseau, pas d’I/O.
# Il sert à :
# - initialiser le package
# - exposer une API propre
# - définir des métadonnées simples

# Exemple (optionnel) :
# Tu pourrais exposer certains objets au niveau du package,
# pour permettre des imports plus simples :
#
# from journey_to_python.models.person import Person
#
# Ce qui permettrait ensuite :
#   from journey_to_python import Person
#
# Mais attention :
# - ne fais ça que pour les objets "publics"
# - évite de tout exposer inutilement

# Tu peux aussi définir la version du package ici :
#
# __version__ = "0.1.0"
#
# Cette valeur peut ensuite être utilisée :
# - dans la CLI (commande `version`)
# - dans la documentation
# - dans les logs
#
# Pour l’instant, on laisse ce fichier volontairement vide
# (à part les commentaires), ce qui est parfaitement correct.
