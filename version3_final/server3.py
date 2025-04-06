import socket  # Module pour les sockets
import subprocess  # Module pour exécuter des scripts
import time  # Module pour les timestamps
import threading  # Module pour la planification

# Configuration réseau et données
HOST = "localhost"
PORT = 5000
USERS = {"alice": "pass123", "bob": "pass456"}
sessions = {}
history = []
scheduled_tasks = []  # Liste pour suivre les tâches planifiées (non utilisée ici)

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

def schedule_task(user, script, delay):
    """
    Planifie une tâche pour s'exécuter après un délai.
    :param user: Utilisateur qui a planifié
    :param script: Script à exécuter
    :param delay: Délai en secondes
    """
    def task():
        result = run_script(script)
        history.append({"user": user, "script": script, "result": result, "time": time.ctime()})
    threading.Timer(delay, task).start()  # Lance un timer

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Serveur en écoute sur {HOST}:{PORT}")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connexion de {addr}")

        data = client_socket.recv(1024).decode("utf-8")
        parts = data.split("|", 1)
        command = parts[0]
        if command == "LOGIN":
            user, password = parts[1].split(":", 1)
            if authenticate(user, password):
                session_id = f"{user}_{int(time.time())}"
                sessions[session_id] = user
                client_socket.send(f"OK:{session_id}".encode("utf-8"))
            else:
                client_socket.send("Erreur : Authentification échouée".encode("utf-8"))
        elif command == "RUN":
            session_id, script = parts[1].split(":", 1)
            if session_id in sessions:
                result = run_script(script)
                user = sessions[session_id]
                history.append({"user": user, "script": script, "result": result, "time": time.ctime()})
                client_socket.send(result.encode("utf-8"))
            else:
                client_socket.send("Erreur : Session invalide".encode("utf-8"))
        elif command == "HISTORY":
            session_id = parts[1]
            if session_id in sessions:
                user = sessions[session_id]
                user_history = [f"{h['time']} - {h['script']} -> {h['result']}" 
                               for h in history if h["user"] == user]
                response = "\n".join(user_history) or "Aucun historique"
                client_socket.send(response.encode("utf-8"))
            else:
                client_socket.send("Erreur : Session invalide".encode("utf-8"))
        elif command == "SCHEDULE":
            session_id, rest = parts[1].split(":", 1)
            script, delay = rest.rsplit(":", 1)
            delay = float(delay)  # Convertit le délai en float (secondes)
            if session_id in sessions:
                user = sessions[session_id]
                schedule_task(user, script, delay)
                client_socket.send("Tâche planifiée".encode("utf-8"))
            else:
                client_socket.send("Erreur : Session invalide".encode("utf-8"))

        client_socket.close()
