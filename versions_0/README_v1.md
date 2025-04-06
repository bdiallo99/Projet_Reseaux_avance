# Exécution Distante de Scripts Python - Version 1

## Objectif
Cette version est une implémentation basique d'une application client-serveur utilisant des sockets pour exécuter des scripts Python envoyés par un client sur un serveur.

## Fonctionnalités
- Le serveur écoute sur `localhost:5000` et accepte une connexion à la fois.
- Le client envoie un script Python (ex. `print("Hello")`).
- Le serveur exécute le script avec `python3` et renvoie le résultat ou une erreur.

## Prérequis
- Python 3 installé (`python3 --version` pour vérifier).
- Pas de dépendances supplémentaires.

## Instructions de Test
1. **Lancer le serveur** :
   python3 server.py

#Sortie : Serveur en écoute sur localhost:5000

#Lancer le client Dans un autre terminal :
python3 client.py

#Entrez un script, ex. print("Hello").

#Résultat attendu : Résultat : Success: Hello

#Tests supplémentaires :
#Script avec erreur : print(undefined) → Résultat : Error: Traceback...
#Pas de script (Entrée vide) : Résultat : Error: Aucun script reçu

