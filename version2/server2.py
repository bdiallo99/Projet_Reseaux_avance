import socket  # Module pour les sockets
import subprocess  # Module pour exécuter des scripts
import time  # Module pour générer des timestamps

# Configuration réseau et données
HOST = "localhost"
PORT = 5000
USERS = {"alice": "pass123", "bob": "pass456"}  # Utilisateurs prédéfinis
sessions = {}  # Dictionnaire des sessions actives {session_id: user}
history = []  # Liste pour stocker l'historique des exécutions

def run_script(script):
    """
    Exécute un script Python et renvoie le résultat ou une erreur.
    """
    try:
        result = subprocess.check_output(["python3", "-c", script], stderr=subprocess.STDOUT, text=True)
        return f"Success: {result}"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"
    except FileNotFoundError:
        return "Error: Python interpréteur non trouvé (vérifiez python3)"

def authenticate(user, password):
    """
    Vérifie les identifiants.
    """
    return user in USERS and USERS[user] == password

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Serveur en écoute sur {HOST}:{PORT}")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connexion de {addr}")

        data = client_socket.recv(1024).decode("utf-8")
        parts = data.split("|", 1)  # Sépare la commande des arguments
        command = parts[0]
        if command == "LOGIN":  # Commande de connexion
            user, password = parts[1].split(":", 1)
            if authenticate(user, password):
                session_id = f"{user}_{int(time.time())}"  # Crée un ID de session unique
                sessions[session_id] = user
                client_socket.send(f"OK:{session_id}".encode("utf-8"))
            else:
                client_socket.send("Erreur : Authentification échouée".encode("utf-8"))

        elif command == "RUN":  # Commande d'exécution
            session_id, script = parts[1].split(":", 1)
            if session_id in sessions:
                result = run_script(script)
                user = sessions[session_id]
                history.append({"user": user, "script": script, "result": result, "time": time.ctime()})
                client_socket.send(result.encode("utf-8"))
            else:
                client_socket.send("Erreur : Session invalide".encode("utf-8"))

        elif command == "HISTORY":  # Commande pour voir l'historique
            session_id = parts[1]
            if session_id in sessions:
                user = sessions[session_id]
                user_history = [f"{h['time']} - {h['script']} -> {h['result']}" 
                               for h in history if h["user"] == user]
                response = "\n".join(user_history) or "Aucun historique"
                client_socket.send(response.encode("utf-8"))
            else:
                client_socket.send("Erreur : Session invalide".encode("utf-8"))
        client_socket.close()
