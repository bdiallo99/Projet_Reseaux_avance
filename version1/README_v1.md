# Exécution Distante de Scripts Python - Version 2

## Objectif
Ajoute une authentification simple à la Version 1 pour sécuriser l’accès au serveur.

## Fonctionnalités
- Authentification avec nom d’utilisateur et mot de passe (`alice:pass123`).
- Exécution d’un script Python après authentification réussie.
- Gestion basique des erreurs d’authentification.

## Prérequis
- Python 3 installé.
## Instructions de Test
1. **Lancer le serveur** :
python3 server1.py
Lancer le client :
python3 client1.py

Test réussi : alice / pass123 → Entrez un script Python : print("Hi") → Résultat : Success: Hi
Test échec : alice / wrong → Erreur : Authentification échouée

#Limitations
Pas de sessions persistantes (connexion unique par exécution).
Pas d’historique ni de planification.

