import socket  # Module pour les sockets

# Configuration réseau
HOST = "localhost"
PORT = 5000
session_id = None

def send_command(command):
    """
    Envoie une commande au serveur et renvoie la réponse.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.send(command.encode("utf-8"))
        return client_socket.recv(1024).decode("utf-8")

while True:
    cmd = input("> ").strip().lower()
    if cmd == "login":
        user = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        response = send_command(f"LOGIN|{user}:{password}")
        if response.startswith("OK"):
            session_id = response.split(":")[1]
            print(f"Connecté. Session ID : {session_id}")
        else:
            print(response)
    elif cmd == "run" and session_id:
        script = input("Entrez un script Python : ")
        result = send_command(f"RUN|{session_id}:{script}")
        print("Résultat :", result)
    elif cmd == "history" and session_id:
        result = send_command(f"HISTORY|{session_id}")
        print("Historique :\n", result)
    elif cmd == "schedule" and session_id:
        script = input("Entrez un script Python : ")
        delay = input("Délai en secondes : ")
        result = send_command(f"SCHEDULE|{session_id}:{script}:{delay}")
        print(result)
    elif cmd == "exit":
        break
    else:
        print("Commandes : login, run, history, schedule, exit")
