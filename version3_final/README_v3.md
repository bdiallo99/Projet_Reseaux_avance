# Exécution Distante de Scripts Python - Version 4

## Objectif
Ajoute une planification basique des scripts à la Version 3.

## Fonctionnalités
- Authentification avec sessions.
- Exécution immédiate et historique.
- Planification de scripts avec un délai en secondes.

## Prérequis
- Python 3 installé.

## Instructions de Test
1. **Lancer le serveur** :
   python3 server3.py
Lancer le client :

python3 client3.py

> login → alice / pass123.

> run → print("Now") → Success: Now.

> schedule → print("Later") → 10 → Tâche planifiée.

> history (après 10s) → Affiche les deux exécutions.

> exit
