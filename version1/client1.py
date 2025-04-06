import socket  # Module pour les sockets

# Configuration réseau
HOST = "localhost"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))  # Connexion au serveur
    # Demande des identifiants
    user = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    client_socket.send(f"{user}:{password}".encode("utf-8"))  # Envoie user:password
    response = client_socket.recv(1024).decode("utf-8")  # Reçoit la réponse
    if response == "OK":  # Si authentification réussie
        script = input("Entrez un script Python : ")
        client_socket.send(script.encode("utf-8"))  # Envoie le script
        result = client_socket.recv(1024).decode("utf-8")  # Reçoit le résultat
        print("Résultat :", result)
    else:
        print(response)  # Affiche l'erreur d'authentification
