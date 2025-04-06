# Exécution Distante de Scripts Python - Version 3

## Objectif
Ajoute la gestion des sessions et un historique des exécutions à la Version 2.

## Fonctionnalités
- Authentification avec création d’un ID de session.
- Exécution de scripts avec stockage dans un historique (en mémoire).
- Consultation de l’historique par utilisateur.

## Prérequis
- Python 3 installé.

## Instructions de Test
1. **Lancer le serveur** :
   python3 server2.py
# Lancer le client :
python3 client2.py
> login → alice / pass123 → Session ID.

> run → print("Test") → Success: Test.

> history → Affiche l’historique des exécutions pour alice.

> exit pour sortir 

Limitations
Historique en mémoire (perdu au redémarrage).
Pas de planification.

